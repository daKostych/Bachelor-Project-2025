import os

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
                    return llm_response["parsed"].overall_assessment

            except Exception as e:
                print(f"Error processing blog \"{blog.title_blog}\":\n{e}\nRetrying...")

        print(f"Failed to get valid assessment after the maximum number of attempts {max_retries}.\n"
              f"Blog with ID: {blog.id} is not evaluated.")
        return -1

    llm_assessment = []

    # Process each blog in the DataFrame
    for index, blog in df.iterrows():
        result = process_blog(blog)
        if result == -1:
            print(f"Stopping experiment.")
            llm_assessment.append(-1)
            break

        llm_assessment.append(result)

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
    valid_blogs = blogs[blogs["engagement_level"].isin(["Very Good", "Excellent"])].copy()
    valid_blogs["full_paper"] = valid_blogs["url_paper"].apply(extract_paper_text)

    elements = []
    for text, blog_url, author in zip(valid_blogs["full_paper"],
                                      valid_blogs["url_blog"],
                                      valid_blogs["author_blog"]):
        metadata = {
            "blog_url": blog_url,
            "author": author
        }
        elements.append((text, metadata))

    vector_store = FAISS.from_texts(
        texts=[element[0] for element in elements],
        embedding=langchain_embedding_model,
        metadatas=[element[1] for element in elements]
    )

    vector_store.save_local(VECTOR_STORE_PATH)
    return vector_store
#=======================================================================================================================
def load_or_create_vector_store(vector_store_path=VECTOR_STORE_PATH):
    """Loads the FAISS vector store or creates it if it doesn't exist."""
    if os.path.exists(vector_store_path):
        print("Loading vector store...")
        try:
            vector_store = FAISS.load_local(vector_store_path,
                                            embeddings=langchain_embedding_model,
                                            allow_dangerous_deserialization=True)
            print("Vector store loaded successfully.")
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise
    else:
        print("Vector store does not exist. Creating new one...")
        try:
            vector_store = create_vector_store()
            print("New vector store created successfully.")
        except Exception as e:
            print(f"Error creating vector store: {e}")
            raise
    return vector_store
#=======================================================================================================================