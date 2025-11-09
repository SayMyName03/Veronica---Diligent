"""
Test script to verify setup and components
"""
import os
from config import Config
from document_processor import DocumentProcessor
from llm_manager import LLMManager

def test_configuration():
    """Test configuration"""
    print("=" * 50)
    print("Testing Configuration...")
    print("=" * 50)
    
    Config.validate()
    
    print(f"✓ Ollama Model: {Config.OLLAMA_MODEL}")
    print(f"✓ Ollama URL: {Config.OLLAMA_BASE_URL}")
    print(f"✓ Embedding Model: {Config.EMBEDDING_MODEL}")
    print(f"✓ Chunk Size: {Config.CHUNK_SIZE}")
    
    if Config.PINECONE_API_KEY:
        print(f"✓ Pinecone API Key: {'*' * 20}{Config.PINECONE_API_KEY[-4:]}")
    else:
        print("⚠ Warning: Pinecone API Key not set")
    
    print()

def test_ollama():
    """Test Ollama connection"""
    print("=" * 50)
    print("Testing Ollama Connection...")
    print("=" * 50)
    
    try:
        llm_manager = LLMManager()
        if llm_manager.test_connection():
            print("✓ Ollama is running and accessible!")
            
            # Test a simple query
            print("\nTesting a simple query...")
            response = llm_manager.llm.invoke("Say 'Hello, I am your AI assistant!' in one sentence.")
            print(f"Response: {response}")
            print()
        else:
            print("✗ Cannot connect to Ollama")
            print("  Make sure Ollama is installed and running")
            print("  Install: https://ollama.ai")
            print(f"  Run: ollama pull {Config.OLLAMA_MODEL}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    print()

def test_document_processor():
    """Test document processor"""
    print("=" * 50)
    print("Testing Document Processor...")
    print("=" * 50)
    
    try:
        processor = DocumentProcessor()
        print("✓ Document processor initialized")
        print(f"  Chunk Size: {processor.text_splitter._chunk_size}")
        print(f"  Chunk Overlap: {processor.text_splitter._chunk_overlap}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    print()

def test_pinecone():
    """Test Pinecone connection"""
    print("=" * 50)
    print("Testing Pinecone Connection...")
    print("=" * 50)
    
    if not Config.PINECONE_API_KEY:
        print("⚠ Skipping: Pinecone API Key not configured")
        print("  Add your API key to .env file")
        print()
        return
    
    try:
        from vector_store import VectorStoreManager
        vector_store = VectorStoreManager()
        
        if vector_store.pc:
            print("✓ Pinecone connected successfully!")
            print(f"  Index: {Config.PINECONE_INDEX_NAME}")
        else:
            print("✗ Pinecone connection failed")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    print()

def main():
    """Run all tests"""
    print("\n")
    print("🔍 AI Assistant - System Check")
    print("=" * 50)
    print()
    
    test_configuration()
    test_document_processor()
    test_ollama()
    test_pinecone()
    
    print("=" * 50)
    print("System check complete!")
    print("=" * 50)
    print("\nIf all tests passed, you can run the app with:")
    print("  streamlit run app.py")
    print()

if __name__ == "__main__":
    main()
