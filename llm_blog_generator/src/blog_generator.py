import datetime
import os.path
from datetime import datetime

from src.helpers import get_examples, load_or_create_vector_store
from src.models_setup import gemini_2_flash, embedding_model
from src.text_extraction import *
from src.prompts import prompt_zero_cot, prompt_rag, prompt_retry, prompt_retry_with_memory_usage
from src.config import *
from src.output_formats import *
from src.long_term_memory import LongTermMemory
#=======================================================================================================================
class BlogGenerator:
    """Generate engagement blog from scientific paper"""
    def __init__(self,
                 evaluator=gemini_2_flash, generator=gemini_2_flash,
                 max_attempts=5, max_attempts_call=3,
                 experiment=False, use_memory=False, use_reflexion=False):
        """Initializes the BlogGenerator object with configuration for blog generation and evaluation."""
        self.__generator = generator.with_structured_output(BlogGeneration, include_raw=True)
        self.__evaluator = evaluator.with_structured_output(BlogClassificationCoT, include_raw=True)

        self.__generator_init_prompt = prompt_rag
        self.__generator_retry_prompt = (prompt_retry_with_memory_usage if use_memory else prompt_retry)
        self.__evaluator_prompt = prompt_zero_cot

        self.max_attempts = max_attempts
        self.__max_attempts_call = max_attempts_call

        self.__start_time = None
        self.__token_usage = 0
        self.__request_cnt = 0
        self.__total_request_cnt = 0

        self.__vector_store = load_or_create_vector_store()

        self.experiment_mode = experiment
        self.__use_reflexion = None
        self.__use_memory = None
        self.set_usage_of_reflexion(use_reflexion)
        self.set_usage_of_memory(use_memory)

        self.__memory = LongTermMemory()

        self.__result_blog_path = f"{RESULTS_PATH}/blog"

        print("BlogGenerator initialized with vector store.")

    def set_usage_of_memory(self, bool_value):
        """Setter for configuration parameter self.__use_memory"""
        self.__generator_retry_prompt = (prompt_retry_with_memory_usage if bool_value else prompt_retry)
        self.__use_memory = bool_value
        if bool_value and not self.__use_reflexion:
            self.__use_reflexion = True
            print(f"\"use_reflexion\" parameter is set to \"True\", "
                  f"because long-term memory module can not be used without reflexion mechanism.")

    def set_usage_of_reflexion(self, bool_value):
        """Setter for configuration parameter self.__use_reflexion"""
        self.__use_reflexion = bool_value
        if not bool_value and self.__use_memory:
            self.__use_memory = False
            print(f"\"use_memory\" parameter is set to \"False\", "
                  f"because long-term memory module can not be used without reflexion mechanism.")

    def save_memory(self):
        """Saves memory to disk."""
        self.__memory.save_to_disk()

    def get_relevant_memory_context(self, blog):
        """
        Retrieves the most relevant memory context for a given blog, including the most similar blog and its metadata.
        """
        similar_blog, metadata = self.__memory.retrieve_memory(blog)
        return similar_blog, metadata

    def find_most_similar_article(self, query_text):
        """Finds the most similar article to the provided query text in the vector store."""
        query_embedding = embedding_model.encode(query_text, clean_up_tokenization_spaces=True)
        results = self.__vector_store.similarity_search_by_vector(query_embedding, k=2)

        if results:
            most_similar = results[(1 if self.experiment_mode else 0)]
            print(f"Found most similar article.")
            return most_similar.page_content, most_similar.metadata
        else:
            print("No similar article found.")
            return None

    def sleep_if_need(self, current_time, limit_type):
        """Sleep until the next minute if elapsed seconds from the start point is positive number"""
        elapsed_seconds = (current_time - self.__start_time).total_seconds() if self.__start_time is not None else 0
        sleep_time = 60 - elapsed_seconds if self.__start_time else 60
        if elapsed_seconds > 0:
            print(f"{limit_type} limit exceeded, sleeping for {round(sleep_time)} seconds.")
            time.sleep(sleep_time)

    def check_limits(self):
        """
        Check if the request exceeds the daily, minute or token limits.
        If limits are exceeded, the process is paused until the limits are reset.
        """
        current_time = datetime.now()

        # Check for daily limit (RPD)
        if self.__total_request_cnt >= GEMINI_2_FLASH_RPD:
            print("Daily request limit exceeded!")
            raise Exception("Daily request limit exceeded")

        # Check for RPM limit (Requests per minute)
        if self.__request_cnt >= GEMINI_2_FLASH_RPM:
            self.sleep_if_need(current_time, "RPM")

        # Check for TPM limit (Tokens per minute)
        if self.__token_usage >= GEMINI_2_FLASH_TPM:
            self.sleep_if_need(current_time, "TPM")

    def safe_invoke(self, chain, prompt_variables):
        """Invoke the model while respecting the RPD, RPM, and TPM limits."""
        print("Checking request limits before invoking the model...")
        self.check_limits()

        print("Invoking the model...")
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

        print(f"Model invoked successfully. Total requests today: {self.__total_request_cnt}, RPM: {self.__request_cnt}, TPM: {self.__token_usage}")
        return response

    def handle_call_limit(self, entity, attempt, e):
        """Rate limit checker"""
        if attempt + 1 == self.__max_attempts_call:
            print(f"{e}\nError: Failed to get valid response from {entity} after the maximum number of attempts.")
            return None, None
        else:
            print(f"{e}\nError: Failed to get valid response from {entity} after {attempt + 1} attempts."
              f"\nRetrying...")
            return "Retry", "Retry"

    def generate_blog(self, paper_url=None, paper_text=None):
        """Generates a blog post based on a scientific paper, using retries and prompt refinement."""
        print("-" * 10)
        if paper_url and not paper_text:
            print(f"Extracting paper text from URL: {paper_url}")
            paper_text = extract_paper_text(paper_url)

        examples = get_examples()
        attempts = 0
        best_blog, blog = None, None
        best_engagement_level, engagement_level = "Bad", None
        possible_improvements = None
        assessment_history = []
        best_assessment_history = []

        generation_chain = self.__generator_init_prompt | self.__generator
        evaluation_chain = self.__evaluator_prompt | self.__evaluator

        # Find a relevant example blog for the first generation
        example_paper, example_blog_metadata = self.find_most_similar_article(paper_text)
        example_blog = example_blog_metadata["blog_full_text"]

        while attempts < self.max_attempts:
            print(f"Attempt number {attempts + 1}: Generating blog...")

            for attempt_call in range(self.__max_attempts_call):
                try:
                    if attempts >= 1 and self.__use_reflexion:
                        generation_chain = self.__generator_retry_prompt | self.__generator
                        if not self.__use_memory:
                            print("Using retry prompt with Reflexion...")
                            generator_response = self.safe_invoke(generation_chain,
                                                                  {
                                                                      "generated_blog": blog,
                                                                      "possible_improvements": possible_improvements
                                                                  })
                        else:
                            print("Using retry prompt with Reflexion and memory module...")
                            similar_blog, metadata = self.get_relevant_memory_context(blog)
                            generator_response = self.safe_invoke(generation_chain,
                                                                  {
                                                                      "generated_blog": blog,
                                                                      "possible_improvements": possible_improvements,
                                                                      "similar_blog": similar_blog,
                                                                      "similar_blog_score":
                                                                          metadata["overall_assessment"],
                                                                      "similar_blog_improvements":
                                                                          metadata["improvements"]
                                                                  })
                    else:
                        print("Using RAG prompt...")
                        generator_response = self.safe_invoke(generation_chain,
                                                              {
                                                                  "paper_text": paper_text,
                                                                  "example_paper": example_paper,
                                                                  "example_blog": example_blog
                                                              })
                    if generator_response:
                        blog = generator_response["parsed"].text
                        print("Blog generated successfully.")
                        break
                except Exception as e:
                    history, best_history = self.handle_call_limit("generator", attempt_call, e)
                    if not history and not best_history and self.experiment_mode:
                        return history, best_history
                    elif not history and not best_history:
                        blog = None

            if not blog:
                break

            if self.max_attempts != 1:
                metadata = {}
                content = None
                for attempt_call in range(self.__max_attempts_call):
                    try:
                        evaluator_response = self.safe_invoke(evaluation_chain,
                                                              {
                                                                  "blog_text" : blog,
                                                                  **examples
                                                              })
                        if evaluator_response:
                            content = evaluator_response["parsed"]
                            engagement_level = content.overall_assessment
                            assessment_history.append(CLASSIFICATION_MAP[engagement_level])
                            possible_improvements = "\n".join(
                                [f"{i+1}. {improvement}" for i, improvement in enumerate(content.improvements)]
                            )
                            print(f"Blog evaluated successfully. Evaluation: {engagement_level}.")
                            metadata = {
                                "overall_assessment": content.overall_assessment,
                                "improvements": possible_improvements
                            }
                            break
                    except Exception as e:
                        history, best_history = self.handle_call_limit("evaluator", attempt_call, e)
                        if not history and not best_history and self.experiment_mode:
                            return history, best_history
                        elif not history and not best_history:
                            content = None

                if not content:
                    break

                try:
                    self.__memory.add_to_memory(blog, metadata)
                except Exception as e:
                    print(f"{e}\nError: Failed to add new blog to memory.")

                # If the engagement level is "Very Good" or better, and it is not an experiment, return the blog
                if (engagement_level in ["Very Good", "Excellent"]) and (not self.experiment_mode):
                    print(f"Saving blog in file: {self.__result_blog_path}")
                    with open(self.__result_blog_path, "w", encoding="utf-8") as file:
                        file.write(blog)
                    self.save_memory()
                    return blog

                if CLASSIFICATION_MAP[engagement_level] >= CLASSIFICATION_MAP[best_engagement_level]:
                    best_engagement_level = engagement_level
                    best_blog = blog

                best_assessment_history.append(CLASSIFICATION_MAP[best_engagement_level])

                if not self.experiment_mode:
                    if attempts + 1 == self.max_attempts:
                        print(f"Failed to generate at least \"Very Good\" blog after the maximum number of attempts."
                              f"Best engagement level in previous attempts: {best_engagement_level}")
                    else:
                        print(f"Blog generation attempt {attempts + 1} unsuccessful. Retrying...")

            attempts += 1

        self.save_memory()

        if best_blog:
            print(f"Saving best blog in file: {self.__result_blog_path}")
            with open(self.__result_blog_path, "w", encoding="utf-8") as file:
                file.write(best_blog)
        elif not best_blog and blog:
            best_blog = blog
            print(f"Saving blog in file: {self.__result_blog_path}")
            with open(self.__result_blog_path, "w", encoding="utf-8") as file:
                file.write(blog)
        elif not best_blog and not blog:
            print(f"Unsuccessful generation of the blog, please try again.")
            if os.path.exists(self.__result_blog_path):
                open(self.__result_blog_path, "w").close()

        if self.experiment_mode:
            return assessment_history, best_assessment_history
        else:
            print(f"Generated blog is saved in file: {self.__result_blog_path}")
            return best_blog