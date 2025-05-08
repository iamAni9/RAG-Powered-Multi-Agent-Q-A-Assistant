from agent import QAAgent
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Assistant:
    def __init__(self):
        self.agent = QAAgent()
        
    def ask(self, question):
        logger.info(f"Processing question: {question}")
        result = self.agent.route(question)
        
        logger.info(f"Query routed to: {result['type']}")
        if result["sources"]:
            logger.info(f"Retrieved {len(result['sources'])} source chunks")
        
        return result

if __name__ == "__main__":
    assistant = Assistant()
    while True:
        question = input("\nAsk a question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        
        response = assistant.ask(question)
        print(f"\nAnswer ({response['type']}): {response['answer']}")
        
        if response["sources"]:
            print("\nSources:")
            for i, source in enumerate(response["sources"], 1):
                print(f"{i}. {source.page_content[:200]}...")
        