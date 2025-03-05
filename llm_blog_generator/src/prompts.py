from langchain.prompts import PromptTemplate
#=======================================================================================================================
prompt_simple_answer = PromptTemplate(
    input_variables=["blog_text"],
    template="Rate this blog post in one word."
             "\n"
             "\n"
             "{blog_text}"
)
#=======================================================================================================================
prompt_numeric_rating = PromptTemplate(
    input_variables=["blog_text"],
    template="Rate this blog post in one word and add a numerical rating."
             "\n"
             "\n"
             "{blog_text}"
)
#=======================================================================================================================
prompt_short_comment = PromptTemplate(
    input_variables=["blog_text"],
    template="Rate this blog post on a scale from 1 to 100. Write a short comment to your assessment."
             "\n"
             "\n"
             "{blog_text}"
)
#=======================================================================================================================
prompt_engagement_score = PromptTemplate(
    input_variables=["blog_text"],
    template="Analyze the engagement level of this blog. Rate it on a scale from 1 to 100. "
             "Write a short comment to your assessment."
             "\n"
             "\n"
             "{blog_text}"
)
#=======================================================================================================================
prompt_criteria = PromptTemplate(
    input_variables=["blog_text"],
    template="Analyze the engagement level of this blog based on factors such as readability, structure, attractiveness "
             "of the blog title, clarity, audience appeal, and potential for discussion. "
             "Rate it on a scale from 1 to 100. Write a short comment to your assessment."
             "\n"
             "\n"
             "{blog_text}"
)
#=======================================================================================================================
prompt_separate_assessment = PromptTemplate(
    input_variables=["blog_text"],
    template="Analyze the engagement level of this blog on a scale from 1 to 100 based on the following criteria:\n"
             " - Readability\n"
             " - Structure\n"
             " - Informativeness\n"
             " - Attractiveness of the blog title\n"
             " - Clarity\n"
             " - Audience appeal\n"
             " - Potential for discussion\n"
             "Provide separate score for each criterion. Then accumulate them into one overall assessment.\n"
             "\n"
             "Blog:\n"
             "{blog_text}\n"
)
#=======================================================================================================================
prompt_with_profile = PromptTemplate(
    input_variables=["blog_text"],
    template="You are an expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.\n"
             "\n"
             "Analyze the engagement level of this blog on a scale from 1 to 100 based on the following criteria:\n"
             " - Readability\n"
             " - Structure\n"
             " - Informativeness\n"
             " - Attractiveness of the blog title\n"
             " - Clarity\n"
             " - Audience appeal\n"
             " - Potential for discussion\n"
             "Provide separate score for each criterion. Then accumulate them into one overall assessment.\n"
             "\n"
             "Blog:\n"
             "{blog_text}\n"
)
#=======================================================================================================================
prompt_structured_sections = PromptTemplate(
    input_variables=["blog_text"],
    template="You are an expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.\n"
             "\n"
             "Task:\n"
             "Analyze the engagement level of the blog below on a scale from 1 to 100 based on the following criteria:\n"
             " - Readability\n"
             " - Structure\n"
             " - Informativeness\n"
             " - Attractiveness of the blog title\n"
             " - Clarity\n"
             " - Audience appeal\n"
             " - Potential for discussion\n"
             "\n"
             "Expected Output Format:\n"
             " - Provide separate score for each criterion with a short comment.\n"
             " - Then accumulate them into one overall assessment on a scale from 1 to 100.\n"
             " - Write down possible improvements to the blog.\n"
             " - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.\n"
             "\n"
             "Now evaluate the provided blog:\n"
             "\n"
             "Referenced Blog to Evaluate:\n"
             "{blog_text}\n"
)
#=======================================================================================================================
prompt_two_shots = PromptTemplate(
    input_variables=["blog_text",
                     "blog_ex1", "blog_ex2",
                     "score_ex1", "score_ex2"],
    template="You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.\n"
             "\n"
             "Task:\n"
             "Analyze the engagement level of the blog below on a scale from 1 to 100 based on the following criteria:\n"
             " - Readability\n"
             " - Structure\n"
             " - Informativeness\n"
             " - Attractiveness of the blog title\n"
             " - Clarity\n"
             " - Audience appeal\n"
             " - Potential for discussion\n"
             "\n"
             "Expected Output Format:\n"
             " - Accumulate your judgment into one overall assessment on a scale from 1 to 100.\n"
             " - Explain why you gave this assessment.\n"
             " - Write down possible improvements to the blog.\n"
             " - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.\n"
             " - Сalmly lower your blog assessment according to the number of bugs.\n"
             " - Return ONLY a valid JSON object in plain text.\n"
             "\n"
             "Reference Examples:\n"
             "Below are examples of blog evaluations, each representing a different engagement score. Use them as a reference when assessing the provided blog.\n"
             "\n"
             "---\n"
             "Example 1\n"
             "Blog:\n"
             "{blog_ex1}\n"
             "\n"
             "Engagement Score: {score_ex1}/100\n"
             "---\n"
             "\n"
             "Example 2\n"
             "Blog:\n"
             "{blog_ex2}\n"
             "\n"
             "Engagement Score: {score_ex2}/100\n"
             "---\n"
             "\n"
             "Now evaluate the provided blog:\n"
             "\n"
             "Referenced Blog to Evaluate:\n"
             "{blog_text}\n"
)
#=======================================================================================================================
prompt_five_shots = PromptTemplate(
    input_variables=["blog_text", "excellent_blog", "very_good_blog", "good_blog", "average_blog", "bad_blog"],
    template="You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.\n"
             "\n"
             "Task:\n"
             "Analyze the engagement level of the blog below based on the following criteria:\n"
             " - Readability\n"
             " - Structure\n"
             " - Informativeness\n"
             " - Attractiveness of the blog title\n"
             " - Clarity\n"
             " - Audience appeal\n"
             " - Potential for discussion\n"
             "\n"
             "Expected Output Format:\n"
             " - Summarize the overall engagement level using one of the following ratings: \"Excellent\", \"Very Good\", \"Good\", \"Average\", \"Bad\".\n"
             " - Explain why you gave this assessment.\n"
             " - Write down possible improvements to the blog.\n"
             " - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.\n"
             " - Сalmly lower your blog assessment according to the number of bugs.\n"
             " - Return ONLY a valid JSON object in plain text.\n"
             "\n"
             "Reference Examples:\n"
             "Below are examples of blog evaluations, each representing a different engagement level. Use them as a reference when assessing the provided blog.\n"
             "\n"
             "---\n"
             "Example 1 (Excellent)\n"
             "Blog:\n"
             "{excellent_blog}\n"
             "\n"
             "Engagement level: Excellent\n"
             "---\n"
             "\n"
             "Example 2 (Very Good)\n"
             "Blog:\n"
             "{very_good_blog}\n"
             "\n"
             "Engagement level: Very Good\n"
             "---\n"
             "\n"
             "Example 3 (Good)\n"
             "Blog:\n"
             "{good_blog}\n"
             "\n"
             "Engagement level: Good\n"
             "---\n"
             "\n"
             "Example 4 (Average)\n"
             "Blog:\n"
             "{average_blog}\n"
             "\n"
             "Engagement level: Average\n"
             "---\n"
             "\n"
             "Example 5 (Bad)\n"
             "Blog:\n"
             "{bad_blog}\n"
             "\n"
             "Engagement level: Bad\n"
             "---\n"
             "\n"
             "Now evaluate the provided blog:\n"
             "\n"
             "Referenced Blog to Evaluate:\n"
             "{blog_text}\n"
)
#=======================================================================================================================