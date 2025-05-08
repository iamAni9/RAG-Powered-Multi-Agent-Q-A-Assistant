from retriever import Retriever
from config import Config
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import re, requests

class QAAgent:
    def __init__(self):
        self.retriever = Retriever()
        self.config = Config()
        self.llm = ChatGroq(temperature=0, groq_api_key=self.config.GROQ_API, model_name=self.config.GROQ_MODEL)
        
    def route(self, query):
        if self.is_calculation_query(query):
            return {
                "type": "calculation",
                "answer": self.calculate(query),
                "sources": []
            }
        elif self.is_definition_query(query):
            return {
                "type": "definition",
                "answer": self.get_definition(query),
                "sources": []
            }
        else:
            result = self.rag_answer(query)
            return {
                "type": "rag",
                "answer": result["answer"],
                "sources": result["sources"]
            }
        
    def is_calculation_query(self, query):
        calc_pattern = r'\b(calculate|compute|solve|sum|add|multiply|divide|plus|minus|times)\b|\d+\s*[\+\-\*\/]\s*\d+'
        return re.search(calc_pattern, query, re.IGNORECASE) is not None
    
    def is_definition_query(self, query):
        def_pattern = r'\b(define|definition|what is|who is)\b'
        return re.search(def_pattern, query, re.IGNORECASE) is not None
    
    def calculate(self, query):
        try:
            numbers = [float(num) for num in re.findall(r'\d+\.?\d*', query)]
            if 'add' in query or '+' in query or 'sum' in query:
                return str(sum(numbers))
            elif 'subtract' in query or '-' in query:
                return str(numbers[0] - numbers[1])
            elif 'multiply' in query or '*' in query:
                return str(numbers[0] * numbers[1])
            elif 'divide' in query or '/' in query:
                return str(numbers[0] / numbers[1])
            else:
                return "Calculation method not recognized. Please be more specific."
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def get_definition(self, query):
        try:
            match = re.search(r'(define|what is|who is|explain)\s+(.+)', query, re.IGNORECASE)
            if not match:
                return "Please specify a term to define."
            
            term = match.group(2).strip()
            response = requests.get(f"{self.config.DICTIONARY_URL}/{requests.utils.quote(term)}")
            response.raise_for_status() 
            data = response.json()
            if isinstance(data, list):
                meanings = data[0].get('meanings', [])
                if meanings:
                    return meanings[0]['definitions'][0]['definition']
            return "No definition found"
        except Exception as e:
            print(e)
    
    def rag_answer(self, query):
        qa_chain = RetrievalQA.from_chain_type(self.llm, retriever=self.retriever.setup_retriever(), return_source_documents=True)
        result = qa_chain.invoke({"query": query})
        return {
            "answer": result["result"],
            "sources": result["source_documents"]
        }
        