from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Literal
from src.config import GEMINI_2_FLASH, GEMINI_2_FLASH_TEMPERATURE, RATE_LIMIT_RPS, RATE_LIMIT_BUCKET
#=======================================================================================================================
# Do not work
"""class CriterionEvaluation(BaseModel):
    \"""Rating a blog based on one criterion\"""
    criterion: str = Field(..., description="Name of the criterion")
    classification: Literal["Excellent", "Very Good", "Good", "Average", "Bad"] = (
        Field(..., description="Categorical classification of the blog based on the given criterion"))
    comment: str = Field(..., description="Short comment on the blog's assessment based on a given criterion")"""
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
class BlogEvaluation(BaseModel):
    """Comprehensive blog assessment on a scale from 1 to 100"""
    blog_title: str = Field(..., description="Blog title")
    assessment_explanation: str = Field(..., description="Explanation of the assessment")
    overall_assessment: float = (
        Field(..., description="Overall assessment of the blog on a scale from 1.0 to 100.0"))
    improvements: List[str] = Field(..., description="Suggested improvements for the blog")
#=======================================================================================================================
# API request limit
rate_limiter = InMemoryRateLimiter(
    requests_per_second=RATE_LIMIT_RPS,
    max_bucket_size=RATE_LIMIT_BUCKET,
)
#=======================================================================================================================
# Initializing the LLM model
gemini_2_flash = ChatGoogleGenerativeAI(
    model=GEMINI_2_FLASH,
    temperature=GEMINI_2_FLASH_TEMPERATURE,
    rate_limiter=rate_limiter
)
#=======================================================================================================================