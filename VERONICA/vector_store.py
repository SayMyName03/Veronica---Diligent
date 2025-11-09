"""
Vector store manager using Pinecone
"""
import time
from typing import List
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from pinecone import Pinecone, ServerlessSpec
from config import Config


class VectorStoreManager:
    """Manage vector store operations with Pinecone"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL
        )
        self.pc = None
        self.index = None
        self.vectorstore = None
        
        # Initialize Pinecone if API key is available
        if Config.PINECONE_API_KEY:
            self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and index"""
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
            
            # Check if index exists, create if not
            index_name = Config.PINECONE_INDEX_NAME
            
            if index_name not in self.pc.list_indexes().names():
                print(f"Creating new Pinecone index: {index_name}")
                self.pc.create_index(
                    name=index_name,
                    dimension=384,  # Dimension for all-MiniLM-L6-v2
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=Config.PINECONE_ENVIRONMENT
                    )
                )
                # Wait for index to be ready
                time.sleep(1)
            
            self.index = self.pc.Index(index_name)
            print(f"Connected to Pinecone index: {index_name}")
            
        except Exception as e:
            print(f"Error initializing Pinecone: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add documents to the vector store
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            Success status
        """
        try:
            if not self.pc:
                raise Exception("Pinecone not initialized. Check your API key.")
            
            # Create or update vectorstore
            self.vectorstore = LangchainPinecone.from_documents(
                documents=documents,
                embedding=self.embeddings,
                index_name=Config.PINECONE_INDEX_NAME
            )
            
            print(f"Successfully added {len(documents)} document chunks to vector store")
            return True
            
        except Exception as e:
            print(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        try:
            if not self.vectorstore:
                # Initialize vectorstore from existing index
                self.vectorstore = LangchainPinecone.from_existing_index(
                    index_name=Config.PINECONE_INDEX_NAME,
                    embedding=self.embeddings
                )
            
            results = self.vectorstore.similarity_search(query, k=k)
            return results
            
        except Exception as e:
            print(f"Error performing similarity search: {str(e)}")
            return []
    
    def get_retriever(self, k: int = 4):
        """
        Get a retriever object for use in chains
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever object
        """
        if not self.vectorstore:
            # Initialize vectorstore from existing index
            self.vectorstore = LangchainPinecone.from_existing_index(
                index_name=Config.PINECONE_INDEX_NAME,
                embedding=self.embeddings
            )
        
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
