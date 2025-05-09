from dotenv import load_dotenv
import os

try:
    import streamlit as st
    for key, value in st.secrets.items():
        os.environ[key] = str(value)
except ImportError:
    pass

load_dotenv()

class Config:
    GROQ_API = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "deepseek-r1-distill-llama-70b"
    
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    VECTOR_STORE_PATH = "faiss_index"
    DOCUMENT_DIR = "documents"
    DICTIONARY_URL = os.getenv("FREE_DICTIONARY_API")