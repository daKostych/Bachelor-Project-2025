from src.text_extraction import extract_blog_text
from src.config import EXAMPLES_PATH
#=======================================================================================================================
def extract_llm_assessment(df, prompt_template, model, examples, max_retries=3):
    """Extract model assessment of the blog from formated output"""
    chain = prompt_template | model

    def process_blog(blog):
        for attempt in range(max_retries):
            try:
                tmp = {"blog_text" : extract_blog_text(blog)}
                llm_response = chain.invoke({**examples, **tmp})

                if llm_response:
                    print(f"----------\n"
                        f"Blog ID: {blog.id}\n"
                        f"Blog title: {blog.title_blog}\n"
                        f"Referenced paper title: {blog.title_paper}\n"
                        f"LLM Assessment: {llm_response["parsed"].overall_assessment}\n")
                    return llm_response["parsed"].overall_assessment
                else:
                    print(f"Warning: Received invalid response on attempt {attempt + 1}.\n Retrying...")

            except Exception as e:
                print(f"Error processing blog \"{blog.title_blog}\":\n{e}\n Retrying...")

        print(f"Failed to get valid assessment after {max_retries} attempts.")
        return None

    llm_assessment = df.apply(process_blog, axis=1)
    return llm_assessment
#=======================================================================================================================
def get_examples():
    """"""
    example_files = {
        "excellent_blog": f"{EXAMPLES_PATH}/excellent_blog",
        "very_good_blog": f"{EXAMPLES_PATH}/very_good_blog",
        "good_blog": f"{EXAMPLES_PATH}/good_blog",
        "average_blog": f"{EXAMPLES_PATH}/average_blog",
        "bad_blog": f"{EXAMPLES_PATH}/bad_blog"
    }
    examples = {}
    for key, blog_path in example_files.items():
        try:
            with open(blog_path, "r", encoding="utf-8") as file:
                examples[key] = file.read()
        except FileNotFoundError:
            print(f"Error: File {blog_path} not found.")
            examples[key] = ""
    return examples