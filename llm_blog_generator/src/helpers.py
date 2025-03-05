from src.text_extraction import extract_blog_text
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
                        f"LLM Assessment: {llm_response.overall_assessment}\n")
                    return llm_response.overall_assessment
                else:
                    print(f"Warning: Received invalid response on attempt {attempt + 1}.\n Retrying...")

            except Exception as e:
                print(f"Error processing blog \"{blog.title_blog}\":\n{e}\n Retrying...")

        print(f"Failed to get valid assessment after {max_retries} attempts.")
        return None

    llm_assessment = df.apply(process_blog, axis=1)
    return llm_assessment
#=======================================================================================================================