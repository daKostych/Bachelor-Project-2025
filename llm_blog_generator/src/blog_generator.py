from src.models_setup import gemini_2_flash, BlogClassification
from src.text_extraction import *
from src.prompts import prompt_five_shots
from src.config import CLASSIFICATION_MAP
from src.helpers import get_examples

class BlogGenerator:
    """Generate engagement blog from scientific paper"""
    def __init__(self,
                 evaluator=gemini_2_flash, generator=None,
                 min_engagement_level="Good", max_retries=3, max_retries_call=3):
        self.__generator = None
        if not generator:
            self.__generator = evaluator
        else:
            self.__generator = generator
        self.__evaluator = evaluator.with_structured_output(BlogClassification, include_raw=True)

        self.__generator_init_prompt = None
        self.__generator_retry_prompt = None
        self.__evaluator_prompt = prompt_five_shots

        self.__min_engagement_level = min_engagement_level
        self.__max_retries = max_retries
        self.__max_retries_call = max_retries_call

        self.__start_time = None
        self.__token_usage = None
        self.__request_cnt = None
        self.__total_request_cnt = None

    def refine_prompt(self, engagement_level, possible_improvements):
        """"""
        return None

    def generate_blog(self, paper_url):
        """"""
        paper_text = extract_paper_text(paper_url)
        examples = get_examples()
        retries = 0
        best_blog, blog = None, None
        best_engagement_level, engagement_level = "Bad", None
        possible_improvements = None

        # generation_chain = self.__generator_init_prompt | self.__generator
        evaluation_chain = self.__evaluator_prompt | self.__evaluator

        while retries < self.__max_retries:
            print(f"Attempt number {retries + 1}: Generating blog...")

            generator_response = None
            for attempt in range(self.__max_retries_call):
                try:
                    #if retries >= 1:
                    #    generation_chain = self.__generator_retry_prompt | generator_structured
                    #    generator_response = generation_chain.invoke({})
                    #else:
                    #    generator_response = generation_chain.invoke({})
                    if generator_response:
                        break
                except Exception as e:
                    print(f"{e}\nError: Failed to get valid response after {attempt + 1} attempts.\nRetrying...")

            evaluator_response = None
            for attempt in range(self.__max_retries_call):
                try:
                    evaluator_response = evaluation_chain.invoke({
                        "blog_text" : blog,
                        **examples
                    })
                    if evaluator_response:
                        break
                except Exception as e:
                    print(f"{e}\nError: Failed to get valid response after {attempt + 1} attempts.\nRetrying...")

            usage_metadata = evaluator_response["raw"].usage_metadata

            content = evaluator_response["parsed"]
            engagement_level = content.overall_assessment
            possible_improvements = content.possible_improvements
            if engagement_level in ["Good", "Very Good", "Excellent"]:
                return blog

            if CLASSIFICATION_MAP[engagement_level] >= CLASSIFICATION_MAP[best_engagement_level]:
                best_engagement_level = engagement_level
                best_blog = blog

            print(f"Blog generation after attempt number {retries + 1} was unsuccessful. Repeat generation...")
            self.__generator_retry_prompt = self.refine_prompt(engagement_level, possible_improvements)
            retries += 1

        return best_blog