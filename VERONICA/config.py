"""
Configuration file for the AI Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "notemate-index")
    
    # Ollama Configuration (Local LLM)
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Document Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Paths
    UPLOAD_DIR = "uploads"
    VECTORSTORE_DIR = "vectorstore"
    
    # Embeddings
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.PINECONE_API_KEY:
            print("Warning: PINECONE_API_KEY not set. Please configure .env file.")
        if not cls.PINECONE_ENVIRONMENT:
            print("Warning: PINECONE_ENVIRONMENT not set. Please configure .env file.")
        return True
