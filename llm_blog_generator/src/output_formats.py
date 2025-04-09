from pydantic import BaseModel, Field
from typing import List, Literal
#=======================================================================================================================
class BlogEvaluation(BaseModel):
    """Comprehensive blog assessment on a scale from 1 to 100"""
    blog_title: str = Field(..., description="Blog title")
    assessment_explanation: str = Field(..., description="Explanation of the assessment")
    overall_assessment: float = (
        Field(..., description="Overall assessment of the blog on a scale from 1.0 to 100.0"))
    improvements: List[str] = Field(..., description="Suggested improvements for the blog")
#=======================================================================================================================
class BlogClassification(BaseModel):
    """Comprehensive blog classification"""
    blog_title: str = Field(..., description="Blog title")
    assessment_explanation: str = Field(..., description="Explanation of the assessment")
    overall_assessment: Literal["Excellent", "Very Good", "Good", "Average", "Bad"] = (
        Field(..., description="Overall assessment of the blog"))
    improvements: List[str] = Field(..., description="Suggested improvements for the blog")
#=======================================================================================================================
class BlogClassificationCoT(BaseModel):
    """Evaluation of a blog post based on detailed analysis and reasoning steps"""
    blog_title: str = Field(..., description="Blog title")
    chain_of_thoughts: str = (
        Field(..., description="Step-by-step analysis and reasoning for the evaluation of the blog post"))
    overall_assessment: Literal["Excellent", "Very Good", "Good", "Average", "Bad"] = (
        Field(..., description="Overall assessment of the blog"))
    improvements: List[str] = Field(..., description="Suggested improvements for the blog")
#=======================================================================================================================
class BlogClassificationGK(BaseModel):
    """Evaluation of a blog post based on previous generated knowledge."""
    blog_title: str = Field(..., description="Blog title")
    generated_knowledge: str = (
        Field(..., description="A key analysis related to evaluating the blog"))
    overall_assessment: Literal["Excellent", "Very Good", "Good", "Average", "Bad"] = (
        Field(..., description="Overall assessment of the blog"))
    improvements: List[str] = Field(..., description="Suggested improvements for the blog")
#=======================================================================================================================
class BlogClassificationMP(BaseModel):
    """Evaluation of a blog post based on detailed analysis of criteria"""
    blog_title: str = Field(..., description="Blog title")
    meta_steps: str = (
        Field(..., description="Step-by-step analysis and reasoning for each criterion"))
    overall_assessment: Literal["Excellent", "Very Good", "Good", "Average", "Bad"] = (
        Field(..., description="Overall assessment of the blog"))
    improvements: List[str] = Field(..., description="Suggested improvements for the blog")
#=======================================================================================================================
class BlogGeneration(BaseModel):
    """Generation engagement blog post form scientific paper"""
    text: str = Field(..., description="The full text of the blog post with blog title")
#=======================================================================================================================
