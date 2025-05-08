from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config
import os
from functools import partial

class DocumentProcessor:
    def __init__(self):
        self.config = Config()
    
    def load_documents(self):
        if not os.path.exists(self.config.DOCUMENT_DIR):
            os.makedirs(self.config.DOCUMENT_DIR)
            print(f"Created {self.config.DOCUMENT_DIR} directory. Add your document there.")
            return None

        loader = DirectoryLoader(path=self.config.DOCUMENT_DIR, glob="**/*.txt", loader_cls=partial(TextLoader, encoding="utf-8"))
        documents = loader.load()
        
        if not documents:
            print(f"No documents found in {self.config.DOCUMENT_DIR}.")
            return None
        
        return documents
    
    def chunk_documents(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.config.CHUNK_SIZE, chunk_overlap=self.config.CHUNK_OVERLAP)
        return text_splitter.split_documents(documents)
    
    def process_documents(self):
        documents = self.load_documents()
        if not documents:
            return None
        else:
            return self.chunk_documents(documents)