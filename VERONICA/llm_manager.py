"""
LLM Manager for handling local Ollama models
"""
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from config import Config


class LLMManager:
    """Manage local LLM interactions using Ollama"""
    
    def __init__(self):
        self.llm = Ollama(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0.7,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.qa_chain = None
    
    def create_qa_chain(self, retriever):
        """
        Create a conversational QA chain
        
        Args:
            retriever: Vector store retriever
            
        Returns:
            ConversationalRetrievalChain
        """
        # Custom prompt template
        template = """You are an AI assistant helping users understand their documents. 
Use the following context to answer the question. If you don't know the answer based on the context, 
say "I don't have enough information in the uploaded documents to answer that question."

Context: {context}

Question: {question}

Provide a detailed and helpful answer:"""
        
        QA_PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT}
        )
        
        return self.qa_chain
    
    def ask_question(self, question: str) -> dict:
        """
        Ask a question to the AI assistant
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.qa_chain:
            raise Exception("QA chain not initialized. Please upload documents first.")
        
        try:
            result = self.qa_chain({"question": question})
            return {
                "answer": result["answer"],
                "source_documents": result.get("source_documents", [])
            }
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "source_documents": []
            }
    
    def reset_conversation(self):
        """Reset conversation memory"""
        self.memory.clear()
    
    def test_connection(self) -> bool:
        """Test if Ollama is running and accessible"""
        try:
            response = self.llm.invoke("Hello")
            return True
        except Exception as e:
            print(f"Error connecting to Ollama: {str(e)}")
            return False
