from vector_store import VectorStore
from document_processor import DocumentProcessor

class Retriever:
    def __init__(self):
        self.vector_store = VectorStore()
    
    def setup_retriever(self):
        retriever = self.vector_store.get_retriever()
        
        if not retriever:
            processor = DocumentProcessor()
            chunks = processor.process_documents()
            if chunks:
                self.vector_store.create_vector_store(chunks)
                retriever = self.vector_store.get_retriever()
        
        return retriever
    
    def get_documents(self, query):
        retriever = self.setup_retriever()
        
        if retriever:
            return retriever.get_relevant_documents(query)
    
        return []