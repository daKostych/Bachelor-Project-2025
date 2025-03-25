from langchain.prompts import PromptTemplate
#=======================================================================================================================
prompt_simple_answer = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """Rate this blog post in one word.
    
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_numeric_rating = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """Rate this blog post in one word and add a numerical rating.
    
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_short_comment = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """Rate this blog post on a scale from 1 to 100. Write a short comment to your assessment.
    
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_engagement_score = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """Analyze the engagement level of this blog. Rate it on a scale from 1 to 100. Write a short comment to your assessment.
    
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_criteria = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """Analyze the engagement level of this blog based on factors such as readability, structure, attractiveness of the blog title, clarity, audience appeal, and potential for discussion. Rate it on a scale from 1 to 100. Write a short comment to your assessment.
    
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_separate_assessment = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """Analyze the engagement level of this blog on a scale from 1 to 100 based on the following criteria:
        - Readability
        - Structure
        - Informativeness
        - Attractiveness of the blog title
        - Clarity
        - Audience appeal
        - Potential for discussion
    Provide separate score for each criterion. Then accumulate them into one overall assessment.
    
    Blog:
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_with_profile = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.
    
    Analyze the engagement level of this blog on a scale from 1 to 100 based on the following criteria:
        - Readability
        - Structure
        - Informativeness
        - Attractiveness of the blog title
        - Clarity
        - Audience appeal
        - Potential for discussion
    Provide separate score for each criterion. Then accumulate them into one overall assessment.
    
    Blog:
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_structured_sections = PromptTemplate(
    input_variables=["blog_text"],
    template=
    """You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.
    
    Task:
    Analyze the engagement level of the blog below on a scale from 1 to 100 based on the following criteria:
        - Readability
        - Structure
        - Informativeness
        - Attractiveness of the blog title
        - Clarity
        - Audience appeal
        - Potential for discussion
        
    Expected Output Format:
        - Provide separate score for each criterion with a short comment.
        - Then accumulate them into one overall assessment on a scale from 1 to 100.
        - Write down possible improvements to the blog.
        - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
        
    Now evaluate the provided blog.
    
    Referenced Blog to Evaluate:
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_two_shots = PromptTemplate(
    input_variables=["blog_text",
                     "blog_ex1", "blog_ex2",
                     "score_ex1", "score_ex2"],
    template=
    """You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.
    
    Task:
    Analyze the engagement level of the blog below on a scale from 1 to 100 based on the following criteria:
        - Readability
        - Structure
        - Informativeness
        - Attractiveness of the blog title
        - Clarity
        - Audience appeal
        - Potential for discussion
        
    Expected Output Format:
        - Accumulate your judgment into one overall assessment on a scale from 1 to 100.
        - Explain why you gave this assessment.
        - Write down possible improvements to the blog.
        - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
        - Calmly lower your blog assessment according to the number of bugs.
        - Return ONLY a valid JSON object in plain text.
        
    Reference Examples:
    Below are examples of blog evaluations, each representing a different engagement score. Use them as a reference when assessing the provided blog.
    
    ---
    Example 1
    Blog:
    \"\"\"{blog_ex1}\"\"\"
    
    Engagement Score: 
    \"\"\"{score_ex1}/100\"\"\"
    ---
    
    ---
    Example 2
    Blog:
    \"\"\"{blog_ex2}\"\"\"
    
    Engagement Score:
    \"\"\"{score_ex2}/100\"\"\"
    ---
    
    Now evaluate the provided blog.
    
    Referenced Blog to Evaluate:
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_five_shots = PromptTemplate(
    input_variables=["blog_text", "excellent_blog", "very_good_blog", "good_blog", "average_blog", "bad_blog"],
    template=
    """You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience.
    
    Task:
    Analyze the engagement level of the blog below based on the following criteria:
    - Readability
    - Structure
    - Informativeness
    - Attractiveness of the blog title
    - Clarity
    - Audience appeal
    - Potential for discussion
    
    Expected Output Format:
        - Summarize the overall engagement level using one of the following ratings: "Excellent", "Very Good", "Good", "Average", "Bad".
        - Explain why you gave this assessment.
        - Write down possible improvements to the blog.
        - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
        - Calmly lower your blog assessment according to the number of bugs.
        - Return ONLY a valid JSON object in plain text.
        
    Reference Examples:
    Below are examples of blog evaluations, each representing a different engagement level. Use them as a reference when assessing the provided blog.
    
    ---
    Example 1 (Excellent)
    Blog:
    \"\"\"{excellent_blog}\"\"\"
    
    Engagement level: Excellent
    ---
    
    ---
    Example 2 (Very Good)
    Blog:
    \"\"\"{very_good_blog}\"\"\"
    
    Engagement level: Very Good
    ---
    
    ---
    Example 3 (Good)
    Blog:
    \"\"\"{good_blog}\"\"\"
    
    Engagement level: Good
    ---
    
    ---
    Example 4 (Average)
    Blog:
    \"\"\"{average_blog}\"\"\"
    
    Engagement level: Average
    ---
    
    ---
    Example 5 (Bad)
    Blog:
    \"\"\"{bad_blog}\"\"\"
    
    Engagement level: Bad
    ---
    
    Now evaluate the provided blog.
    
    Referenced Blog to Evaluate:
    \"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================