import logging
import datetime
from datetime import datetime
from src.helpers import get_examples, load_or_create_vector_store
from src.models_setup import gemini_2_flash, embedding_model
from src.text_extraction import *
from src.prompts import prompt_five_shots, prompt_rag, prompt_retry
from src.config import RESULTS_PATH, CLASSIFICATION_MAP, LLM_RPD, LLM_RPM, LLM_TPM
from src.output_formats import BlogClassification, BlogGeneration

class BlogGenerator:
    """Generate engagement blog from scientific paper"""
    def __init__(self,
                 evaluator=gemini_2_flash, generator=None,
                 min_engagement_level="Good", max_retries=3, max_retries_call=3):
        """Initializes the BlogGenerator object with configuration for blog generation and evaluation."""
        self.__generator = None
        if not generator:
            self.__generator = evaluator.with_structured_output(BlogGeneration, include_raw=True)
        else:
            self.__generator = generator.with_structured_output(BlogGeneration, include_raw=True)
        self.__evaluator = evaluator.with_structured_output(BlogClassification, include_raw=True)

        self.__generator_init_prompt = prompt_rag
        self.__generator_retry_prompt = prompt_retry
        self.__evaluator_prompt = prompt_five_shots

        self.__min_engagement_level = min_engagement_level
        self.__max_retries = max_retries
        self.__max_retries_call = max_retries_call

        self.__start_time = None
        self.__token_usage = 0
        self.__request_cnt = 0
        self.__total_request_cnt = 0

        self.__vector_store = load_or_create_vector_store()

        logging.info("BlogGenerator initialized with vector store.")

    def find_most_similar_article(self, query_text):
        """Finds the most similar article to the provided query text in the vector store."""
        query_embedding = embedding_model.encode(query_text, clean_up_tokenization_spaces=True)
        results = self.__vector_store.similarity_search_by_vector(query_embedding, k=2)

        if results:
            most_similar = results[1]
            logging.info(f"Found most similar article.")
            return most_similar.metadata
        else:
            logging.warning("No similar article found.")
            return None

    def check_limits(self):
        """
        Check if the request exceeds the daily, minute or token limits.
        If limits are exceeded, the process is paused until the limits are reset.
        """
        current_time = datetime.now()

        # Check for daily limit (RPD)
        if self.__total_request_cnt >= LLM_RPD:
            logging.error("Daily request limit exceeded!")
            raise Exception("Daily request limit exceeded")

        # Check for RPM limit (Requests per minute)
        if self.__request_cnt >= LLM_RPM:
            # Sleep until the next minute
            sleep_time = 60 - (current_time.second - self.__start_time.second) if self.__start_time else 60
            logging.info(f"RPM limit exceeded, sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)

        # Check for TPM limit (Tokens per minute)
        if self.__token_usage >= LLM_TPM:
            # Sleep until the next minute
            sleep_time = 60 - (current_time.second - self.__start_time.second) if self.__start_time else 60
            logging.info(f"TPM limit exceeded, sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)

    def safe_invoke(self, chain, prompt_variables):
        """Invoke the model while respecting the RPD, RPM, and TPM limits."""
        logging.info("Checking request limits before invoking the model...")
        self.check_limits()

        logging.info("Invoking the model...")
        response = chain.invoke(prompt_variables)

        # Update counters after successful invocation
        self.__total_request_cnt += 1
        if not self.__start_time:
            self.__start_time = datetime.now()

        # Reset counters at the start of each new minute
        difference = datetime.now() - self.__start_time
        if difference.seconds >= 60:
            self.__start_time = datetime.now()
            self.__token_usage = 0
            self.__request_cnt = 0

        self.__request_cnt += 1
        if response:
            self.__token_usage += response["raw"].usage_metadata["total_tokens"]

        logging.info(f"Model invoked successfully. Total requests today: {self.__total_request_cnt}, RPM: {self.__request_cnt}, TPM: {self.__token_usage}")
        return response

    def generate_blog(self, paper_url):
        """Generates a blog post based on a scientific paper, using retries and prompt refinement."""
        logging.info(f"Extracting paper text from URL: {paper_url}")
        paper_text = extract_paper_text(paper_url)
        examples = get_examples()
        retries = 0
        best_blog, blog = None, None
        best_engagement_level, engagement_level = "Bad", None
        possible_improvements = None

        generation_chain = self.__generator_init_prompt | self.__generator
        evaluation_chain = self.__evaluator_prompt | self.__evaluator

        while retries < self.__max_retries:
            logging.info(f"Attempt number {retries + 1}: Generating blog...")

            for attempt in range(self.__max_retries_call):
                try:
                    if retries >= 1:
                        generation_chain = self.__generator_retry_prompt | self.__generator
                        generator_response = self.safe_invoke(generation_chain,
                                                              {
                                                                  "generated_blog": blog,
                                                                  "possible_improvements": possible_improvements
                                                              })
                    else:
                        # Find a relevant example blog
                        generation_example = self.find_most_similar_article(paper_text)
                        example_paper = generation_example["full_text"]
                        example_blog = extract_blog_text(url_blog=generation_example["blog_url"],
                                                         author_blog=generation_example["author"],
                                                         claps=generation_example["claps"],
                                                         comments=generation_example["comments"])
                        generator_response = self.safe_invoke(generation_chain,
                                                              {
                                                                  "paper_text": paper_text,
                                                                  "example_paper": example_paper,
                                                                  "example_blog": example_blog
                                                              })
                    if generator_response:
                        blog = generator_response["parsed"].text
                        logging.info("Blog generated successfully.")
                        break
                except Exception as e:
                    logging.error(f"{e}\nError: Failed to get valid response from generator after {attempt + 1} attempts.\nRetrying...")

            for attempt in range(self.__max_retries_call):
                try:
                    evaluator_response = self.safe_invoke(evaluation_chain,
                                                          {
                                                              "blog_text" : blog,
                                                              **examples
                                                          })
                    if evaluator_response:
                        content = evaluator_response["parsed"]
                        engagement_level = content.overall_assessment
                        possible_improvements = "\n".join(
                            [f"{i+1}. {improvement}" for i, improvement in enumerate(content.improvements)]
                        )
                        logging.info(f"Blog evaluated successfully. Evaluation: {engagement_level}.")
                        break
                except Exception as e:
                    logging.error(f"{e}\nError: Failed to get valid response from evaluator after {attempt + 1} attempts.\nRetrying...")

            # If the engagement level is good or better, return the blog
            if engagement_level in ["Good", "Very Good", "Excellent"]:
                logging.info("Saving blog.")
                with open(f"{RESULTS_PATH}/blog", "w", encoding="utf-8") as file:
                    file.write(blog)
                return blog

            if CLASSIFICATION_MAP[engagement_level] >= CLASSIFICATION_MAP[best_engagement_level]:
                best_engagement_level = engagement_level
                best_blog = blog

            logging.info(f"Blog generation attempt {retries + 1} unsuccessful. Retrying...")
            retries += 1

        if best_blog:
            logging.info("Saving best blog.")
            with open(f"{RESULTS_PATH}/blog", "w", encoding="utf-8") as file:
                file.write(best_blog)
        return best_blog