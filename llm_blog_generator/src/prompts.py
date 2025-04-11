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
        
Clarifications:
    - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
    
Expected Output Format:
    - Provide separate score for each criterion with a short comment.
    - Then accumulate them into one overall assessment on a scale from 1 to 100.
    - Write down possible improvements to the blog.
        
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
        
Clarifications:
    - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
    - Calmly lower your blog assessment according to the number of bugs.
    - Return ONLY a valid JSON object in plain text.
        
Expected Output Format:
    - Accumulate your judgment into one overall assessment on a scale from 1 to 100.
    - Explain why you gave this assessment.
    - Write down a few possible improvements that will improve the engagement score, if necessary (if the overall assessment is less than 100).
        
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
        
Clarifications:
    - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
    - Calmly lower your blog assessment according to the number of bugs.
    - Return ONLY a valid JSON object in plain text.
    
Expected Output Format:
    - Summarize the overall engagement level using one of the following ratings: "Excellent", "Very Good", "Good", "Average", "Bad".
    - Explain why you gave this assessment.
    - Write down a few possible improvements that will improve the engagement level, if necessary (if the overall assessment is worse than "Excellent").
        
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
prompt_zero_cot = PromptTemplate(
    input_variables=["blog_text"],
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
        
Clarifications:
    - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
    - Calmly lower your blog assessment according to the number of bugs.
    - Return ONLY a valid JSON object in plain text.

Expected Output Format:
    - Step by step, explain your analysis for each of the criteria listed above. Start by evaluating readability, then move on to structure, informativeness, and so on. Make sure to detail why you gave the specific score for each criterion and provide reasoning.
    - After completing the analysis for each criterion, summarize the overall engagement level using one of the following ratings: "Excellent", "Very Good", "Good", "Average", "Bad".
    - Write down a few possible improvements that will improve the engagement level, if necessary (if the overall assessment is worse than "Excellent").

Now evaluate the provided blog.

Referenced Blog to Evaluate:
\"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_generated_knowledge = PromptTemplate(
    input_variables=["blog_text"],
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
        
Clarifications:
    - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
    - Calmly lower your blog assessment according to the number of bugs.
    - Return ONLY a valid JSON object in plain text.

Expected Output Format:
    - Before proceeding with the blog evaluation, generate a key analysis related to evaluating the blog based on the criteria mentioned above. Use this generated knowledge during the actual blog evaluation.
    - After completing the analysis for each criterion, summarize the overall engagement level using one of the following ratings: "Excellent", "Very Good", "Good", "Average", "Bad".
    - Write down a few possible improvements that will improve the engagement level, if necessary (if the overall assessment is worse than "Excellent").

Now evaluate the provided blog.

Referenced Blog to Evaluate:
\"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_meta = PromptTemplate(
    input_variables=["blog_text"],
    template=
"""You are a very strict expert in evaluating written content, specializing in assessing how well blogs communicate scientific research to a broader audience. Integrate step-by-step reasoning to evaluate engagement level of the blog below under the following structure.

Clarifications:
    - Focus only on the textual content of the blog, disregarding any visual or interactive elements. This means that there is no need to add points related to the addition of illustrations or interactive elements to possible improvements.
    - Calmly lower your blog assessment according to the number of bugs.
    - Return ONLY a valid JSON object in plain text.

{{
    "Referenced blog to evaluate": "[Blog title]",
    "Step 1": "Analyze the readability of the blog. Is the text easy to understand? Are the sentences clear and well-structured?",
    "Step 2": "Evaluate the structure of the blog. Does it follow a logical flow? Are the sections well-organized?",
    "Step 3": "Consider the informativeness. Does the blog provide valuable, well-researched information?",
    "Step 4": "Analyze the attractiveness of the blog title. Is the title engaging and does it accurately represent the content of the blog?",
    "Step 5": "Evaluate the clarity of the blog. Are the ideas presented clearly, without ambiguity or unnecessary complexity?",
    "Step 6": "Assess the audience appeal. Would the intended audience find the blog interesting? Is the tone appropriate for the target readers?",
    "Step 7": "Consider the potential for discussion. Does the blog invite the reader to engage in further thought or discussion?",
    "Step 8": "After completing the analysis for each criterion, summarize the overall engagement level using one of the following ratings: "Excellent", "Very Good", "Good", "Average", "Bad".",
    "Step 9": "Write down a few possible improvements that will improve the engagement level, if necessary (if the overall assessment is worse than "Excellent").",
    "Overall engagement level": "[Final assessment of the blog as one of the following ratings: "Excellent", "Very Good", "Good", "Average", "Bad"]",
    "Possible improvements": "[List of possible improvements]"
}}

Now evaluate the provided blog.

Referenced Blog to Evaluate:
\"\"\"{blog_text}\"\"\""""
)
#=======================================================================================================================
prompt_rag = PromptTemplate(
    input_variables=["paper_text", "example_paper", "example_blog"],
    template=
"""You are an advanced language model specialized in transforming scientific articles into engaging and accessible blog posts. 
Your primary goal is to maintain scientific accuracy while making the content appealing to a broad audience. Follow these guidelines to create engagement blog posts:

1. Strong Introduction: 
   - Begin with a captivating introduction that includes a thought-provoking question, an interesting fact, or a real-life example related to the research.
   - Use a clear, concise, and intriguing title to capture attention.
2. Simplicity and Clarity:
   - Simplify complex scientific concepts without losing accuracy.
   - Use short and direct sentences for better comprehension.
3. Logical Structure:
   - Break the content into smaller sections with subheadings.
   - Ensure a coherent flow and maintain readability by using brief paragraphs, lists, and bullet points.
4. Emphasis on Key Takeaways:
   - Clearly communicate the primary findings and practical implications of the research.
   - Focus on essential points and avoid overwhelming details.
5. Reader Engagement:
   - Include open-ended questions or calls to action to encourage interaction.
   - Connect the research to real-world applications and potential impacts on people's lives.
   - Encourage readers to share their thoughts or explore the full study.
6. Optimal Length:
   - Aim for a word count between 750 and 1,000 words, keeping the content detailed yet engaging.
    
Below are examples of paired scientific articles and their corresponding blog posts. Use them as reference points when generating engaging and informative blogs from scientific articles.

Scientific article:
\"\"\"{example_paper}\"\"\"

Blog post:
\"\"\"{example_blog}\"\"\"

Now, generate a blog post based on the following scientific article.

Scientific article:
\"\"\"{paper_text}\"\"\"

Blog post:
"""
)
#=======================================================================================================================
prompt_retry = PromptTemplate(
    input_variables=["generated_blog", "possible_improvements"],
    template=
"""You are a highly skilled writing assistant specialized in refining and enhancing blog posts to maximize reader engagement and clarity. 
Your task is to take an already generated blog post and improve it by incorporating suggested changes. 
You will ensure that the revised blog is not only more captivating and informative but also maintains scientific accuracy and coherence.

The generated blog post has been evaluated using a 5-level rating system: \"Bad\", \"Average\", \"Good\", \"Very Good\", and \"Excellent\". 
Your goal is to maximize the rating of the revised blog, aiming to reach the \"Excellent\".

Follow these steps:
1. Carefully review the original generated blog to understand its structure and content.
2. Analyze the provided possible improvements and integrate them into the text.
3. Maintain the original message and key points while integrating suggested improvements.
4. Ensure that the blog remains professional, yet accessible to a broad audience.

Now, rewrite the original generated blog.

Original Generated Blog:
\"\"\"{generated_blog}\"\"\"

Possible Improvements:
\"\"\"{possible_improvements}\"\"\"

Revised Blog:
"""
)
#=======================================================================================================================
prompt_retry_with_memory_usage = PromptTemplate(
    input_variables=["generated_blog", "possible_improvements", "similar_blog", "similar_blog_score", "similar_blog_improvements"],
    template=
"""You are a highly skilled writing assistant specialized in refining and enhancing blog posts to maximize reader engagement and clarity. 
Your task is to take an already generated blog post and improve it by incorporating suggested changes. 
You will ensure that the revised blog is not only more captivating and informative but also maintains scientific accuracy and coherence.

The generated blog post has been evaluated using a 5-level rating system: \"Bad\", \"Average\", \"Good\", \"Very Good\", and \"Excellent\". 
Your goal is to maximize the rating of the revised blog, aiming to reach the \"Excellent\".

Follow these steps:
1. Carefully review the original generated blog to understand its structure and content.
2. Analyze the provided possible improvements and integrate them into the text.
3. Maintain the original message and key points while integrating suggested improvements.
4. Ensure that the blog remains professional, yet accessible to a broad audience.
5. Take into consideration the memory context from the agent's previous experiences, specifically the most similar blog, its evaluation score, and the suggested improvements for it. Use this context to guide you in refining the current blog.

### Memory Context:
Most Similar Blog from Memory:
\"\"\"{similar_blog}\"\"\"

Evaluation of the Similar Blog:
\"\"\"{similar_blog_score}\"\"\"

Suggested Improvements for the Similar Blog:
\"\"\"{similar_blog_improvements}\"\"\"

Now, rewrite the original generated blog.

### Original Generated Blog:
\"\"\"{generated_blog}\"\"\"

### Possible Improvements:
\"\"\"{possible_improvements}\"\"\"

### Revised Blog:
"""
)