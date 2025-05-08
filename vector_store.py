from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config
import os
import shutil

class VectorStore:
    def __init__(self):
        self.config = Config()
        self.embeddings = HuggingFaceEmbeddings(model_name=self.config.EMBEDDING_MODEL)
        self.vector_store = None
        
    def create_vector_store(self, chunks):
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.vector_store.save_local(self.config.VECTOR_STORE_PATH)
        return self.vector_store
    
    def load_existing_vector_store(self):
        if os.path.exists(self.config.VECTOR_STORE_PATH):
            self.vector_store = FAISS.load_local(self.config.VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
            return self.vector_store
        return None
    
    def reset_vector_store(self):
        if os.path.exists(self.config.VECTOR_STORE_PATH):
            shutil.rmtree(self.config.VECTOR_STORE_PATH)
            print(f"Deleted existing vector store at {self.config.VECTOR_STORE_PATH}")
    
    def get_retriever(self, k=3):
        if self.vector_store is None:
            self.vector_store = self.load_existing_vector_store()
        if self.vector_store:
            return self.vector_store.as_retriever(search_kwargs={"k": k})
        return None