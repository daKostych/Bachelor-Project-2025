import os
import logging

from langchain.vectorstores import FAISS

from src.text_extraction import *
from src.config import EXAMPLES_PATH, VECTOR_STORE_PATH, PREPROCESSED_BLOG_DATASET_PATH
from src.models_setup import embedding_model, langchain_embedding_model
#=======================================================================================================================
def extract_llm_assessment(df, prompt_template, model, examples, max_retries=3):
    """Extract model assessment of the blog from formated output"""
    chain = prompt_template | model

    def process_blog(blog):
        for attempt in range(max_retries):
            try:
                tmp = {"blog_text" : blog.blog_full_text}
                llm_response = chain.invoke({**examples, **tmp})

                if llm_response:
                    """print(f"----------\n"
                        f"Blog ID: {blog.id}\n"
                        f"Blog title: {blog.title_blog}\n"
                        f"Referenced paper title: {blog.title_paper}\n"
                        f"LLM Assessment: {llm_response["parsed"].overall_assessment}\n")"""
                    return llm_response["parsed"].overall_assessment
                """else:
                    print(f"Warning: Received invalid response on attempt {attempt + 1}.\n Retrying...")"""

            except Exception as e:
                print(f"Error processing blog \"{blog.title_blog}\":\n{e}\n Retrying...")

        print(f"Failed to get valid assessment after {max_retries} attempts.")
        return None

    llm_assessment = df.apply(process_blog, axis=1)
    return llm_assessment
#=======================================================================================================================
def get_examples():
    """Set examples for five-shot prompt"""
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
#=======================================================================================================================
def create_vector_store():
    """Creates a new FAISS vector store from the provided data."""
    # Data processing
    blogs = pd.read_csv(PREPROCESSED_BLOG_DATASET_PATH)
    valid_blogs = blogs[blogs["engagement_level"].isin(["Good", "Very Good", "Excellent"])].copy()
    valid_blogs["full_paper"] = valid_blogs["url_paper"].apply(extract_paper_text)

    elements = []
    for text, blog_url, author, claps, comments in zip(valid_blogs["full_paper"],
                                                       valid_blogs["url_blog"],
                                                       valid_blogs["author_blog"]):
        embedding = embedding_model.encode(text, clean_up_tokenization_spaces=True)
        metadata = {
            "full_text": text,
            "blog_url": blog_url,
            "author": author
        }
        elements.append((embedding, metadata))

    vector_store = FAISS.from_texts(
        texts=[element[1]["full_text"] for element in elements],
        embedding=langchain_embedding_model,
        metadatas=[element[1] for element in elements]
    )

    vector_store.save_local(VECTOR_STORE_PATH)
    return vector_store
#=======================================================================================================================
def load_or_create_vector_store(vector_store_path=VECTOR_STORE_PATH):
    """Loads the FAISS vector store or creates it if it doesn't exist."""
    if os.path.exists(vector_store_path):
        logging.info("Loading vector store...")
        try:
            vector_store = FAISS.load_local(vector_store_path,
                                            embeddings=langchain_embedding_model,
                                            allow_dangerous_deserialization=True)
            logging.info("Vector store loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading vector store: {e}")
            raise
    else:
        logging.warning("Vector store does not exist. Creating new one...")
        try:
            vector_store = create_vector_store()
            logging.info("New vector store created successfully.")
        except Exception as e:
            logging.error(f"Error creating vector store: {e}")
            raise
    return vector_store
#=======================================================================================================================