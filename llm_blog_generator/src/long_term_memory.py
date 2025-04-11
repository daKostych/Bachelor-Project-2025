from langchain_community.vectorstores import FAISS

from src.models_setup import langchain_embedding_model, embedding_model
from src.config import LONG_TERM_MEMORY_PATH, DISTANCE_THRESHOLD, CLASSIFICATION_MAP
#=======================================================================================================================
class LongTermMemory:
    def __init__(self, vector_store_path=LONG_TERM_MEMORY_PATH, threshold_distance=DISTANCE_THRESHOLD):
        """
        Initializes the LongTermMemory object with the provided vector store path and similarity threshold.
        Loads the existing vector store if available or initializes a new one.
        """
        self.__vector_store_path = vector_store_path
        self.__embedding_model = embedding_model
        self.__langchain_embedding_model = langchain_embedding_model
        self.__vector_store = self.load_vector_store()
        self.__threshold_distance = threshold_distance

    def load_vector_store(self):
        try:
            print(f"Loading long term memory module from: {self.__vector_store_path}")
            vector_store = FAISS.load_local(self.__vector_store_path,
                                            embeddings=self.__langchain_embedding_model,
                                            allow_dangerous_deserialization=True)
            print("Long term memory module loaded successfully.")
        except:
            print(f"Failed to load Long term memory module. Initializing a new one...")

            # Initialize with dummy data to avoid the "list index out of range" error
            dummy_text = "Dummy text to initialize the long term memory."
            dummy_metadata = {}

            # Initialize FAISS with a single dummy item
            vector_store = FAISS.from_texts(texts=[dummy_text],
                                            embedding=self.__langchain_embedding_model,
                                            metadatas=[dummy_metadata])
            print("Long term memory module initialized successfully with dummy data.")
        return vector_store

    def add_to_memory(self, text, metadata):
        """
        Adds a new text and its metadata to memory if it's not too similar to the existing ones.
        If similar texts exist, tries to upsert.
        """
        embedding = self.__embedding_model.encode(text, clean_up_tokenization_spaces=True)
        similar_results = self.__vector_store.similarity_search_with_score_by_vector(embedding, k=2)

        if similar_results and len(similar_results) == 2:
            distances = [result[1] for result in similar_results]
            if all(distance <= self.__threshold_distance for distance in distances):
                print("Found 2 similar blogs. Upsert blog to memory...")
                self.upsert_blog(similar_results, text, metadata, embedding)
            else:
                self.__vector_store.add_texts([text],
                                              metadatas=[metadata],
                                              embeddings=[embedding])
                print("No similar blogs found, new blog is added to memory.")
        else:
            self.__vector_store.add_texts([text],
                                          metadatas=[metadata],
                                          embeddings=[embedding])
            print("No similar blogs found, new blog is added to memory.")

    def upsert_blog(self, similar_results, text, metadata, embedding):
        """
        Takes the best of the three provided insights and leaves it in memory, and deletes the rest.
        """
        best_of_similar_results = max(similar_results,
                                      key=
                                      lambda blog: CLASSIFICATION_MAP.get(blog[0].metadata["overall_assessment"], 0))
        best_assessment = CLASSIFICATION_MAP.get(best_of_similar_results[0].metadata["overall_assessment"], 0)
        if CLASSIFICATION_MAP.get(metadata["overall_assessment"], 0) >= best_assessment:
            ids_to_delete = [result[0].id for result in similar_results]
            print(f"Deleting blogs with ids: {ids_to_delete}")
            self.__vector_store.delete(ids_to_delete)
            self.__vector_store.add_texts([text],
                                          metadatas=[metadata],
                                          embeddings=[embedding])
        else:
            ids_to_delete = [result[0].id for result in similar_results if result != best_of_similar_results]
            print(f"Deleting blogs with ids: {ids_to_delete}")
            self.__vector_store.delete(ids_to_delete)

    def retrieve_memory(self, query_text, k=1):
        """
        Retrieves the most relevant blog from memory based on a query.
        """
        query_embedding = self.__embedding_model.encode(query_text, clean_up_tokenization_spaces=True)
        results = self.__vector_store.similarity_search_by_vector(query_embedding, k)
        if results and len(results) == k:
            print("Found relevant memory.")
            return results[0].page_content, results[0].metadata
        else:
            print("No relevant memory found.")
            return "", {"overall_assessment": "", "improvements": ""}

    def save_to_disk(self):
        """
        Saves the vector store to disk.
        """
        self.__vector_store.save_local(self.__vector_store_path)
        print("Long term memory module saved successfully.")