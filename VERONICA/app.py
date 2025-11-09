"""
Streamlit UI for the AI Assistant (Jarvis-like interface)
"""
import streamlit as st
import os
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from llm_manager import LLMManager
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI Assistant - VERONICA",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.messages = []
    st.session_state.documents_processed = False

def initialize_components():
    """Initialize all components"""
    if not st.session_state.initialized:
        Config.validate()
        st.session_state.doc_processor = DocumentProcessor()
        st.session_state.vector_store = VectorStoreManager()
        st.session_state.llm_manager = LLMManager()
        st.session_state.initialized = True

def main():
    """Main application"""
    initialize_components()
    
    # Title and description
    st.title("🤖 AI Assistant - VERONICA")
    st.markdown("### Your Personal Document AI Assistant")
    st.markdown("Upload your PDF or DOCX files and ask questions about their content!")
    
    # Sidebar for document upload and settings
    with st.sidebar:
        st.header("📁 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload PDF or DOCX files",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True
        )
        auto_process = st.checkbox("Auto-process uploads", value=True, help="Automatically process files as soon as they are uploaded.")
        
        # Auto-process newly uploaded files by detecting a change in the upload signature
        try:
            current_sig = tuple((f.name, len(f.getbuffer())) for f in (uploaded_files or []))
        except Exception:
            current_sig = tuple((f.name, 0) for f in (uploaded_files or []))

        if auto_process and uploaded_files and (current_sig != st.session_state.get("_last_upload_sig")):
            st.session_state["_last_upload_sig"] = current_sig
            with st.spinner("Processing documents..."):
                try:
                    all_documents = []
                    for uploaded_file in uploaded_files:
                        # Save file
                        file_path = st.session_state.doc_processor.save_uploaded_file(
                            uploaded_file,
                            uploaded_file.name
                        )

                        # Process document
                        documents = st.session_state.doc_processor.process_document(file_path)
                        all_documents.extend(documents)
                        st.success(f"✅ Processed: {uploaded_file.name}")

                    # Add to vector store
                    st.session_state.vector_store.add_documents(all_documents)

                    # Create QA chain
                    retriever = st.session_state.vector_store.get_retriever()
                    st.session_state.llm_manager.create_qa_chain(retriever)

                    st.session_state.documents_processed = True
                    st.success(f"🎉 Successfully processed {len(uploaded_files)} document(s)!")
                    st.info(f"Total chunks created: {len(all_documents)}")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

        if st.button("Process Documents", type="primary"):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    try:
                        all_documents = []
                        
                        for uploaded_file in uploaded_files:
                            # Save file
                            file_path = st.session_state.doc_processor.save_uploaded_file(
                                uploaded_file, 
                                uploaded_file.name
                            )
                            
                            # Process document
                            documents = st.session_state.doc_processor.process_document(file_path)
                            all_documents.extend(documents)
                            
                            st.success(f"✅ Processed: {uploaded_file.name}")
                        
                        # Add to vector store
                        st.session_state.vector_store.add_documents(all_documents)
                        
                        # Create QA chain
                        retriever = st.session_state.vector_store.get_retriever()
                        st.session_state.llm_manager.create_qa_chain(retriever)
                        
                        st.session_state.documents_processed = True
                        st.success(f"🎉 Successfully processed {len(uploaded_files)} document(s)!")
                        st.info(f"Total chunks created: {len(all_documents)}")
                        
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
            else:
                st.warning("Please upload at least one document.")
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        
        # Test Ollama connection
        if st.button("Test LLM Connection"):
            with st.spinner("Testing Ollama connection..."):
                if st.session_state.llm_manager.test_connection():
                    st.success("✅ Ollama is running!")
                else:
                    st.error("❌ Cannot connect to Ollama. Make sure it's running.")
        
        # Reset conversation
        if st.button("Reset Conversation"):
            st.session_state.llm_manager.reset_conversation()
            st.session_state.messages = []
            st.success("Conversation reset!")
        
        st.divider()
        
        # Status
        st.header("📊 Status")
        st.write(f"LLM Model: {Config.OLLAMA_MODEL}")
        st.write(f"Documents Processed: {'✅' if st.session_state.documents_processed else '❌'}")
        st.write(f"Vector Store: {'✅ Connected' if st.session_state.vector_store.pc else '❌ Not Connected'}")
    
    # Main chat interface
    if st.session_state.documents_processed:
        st.markdown("### 💬 Ask Questions About Your Documents")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Source Documents"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:** {source.metadata.get('source', 'Unknown')}")
                            st.text(source.page_content[:200] + "...")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = st.session_state.llm_manager.ask_question(prompt)
                    answer = result["answer"]
                    sources = result["source_documents"]
                    
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("📚 Source Documents"):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**Source {i}:** {source.metadata.get('source', 'Unknown')}")
                                st.text(source.page_content[:200] + "...")
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
    else:
        st.info("👈 Please upload and process documents from the sidebar to start chatting!")
        
        # Instructions
        st.markdown("""
        ### 📝 How to Use:
        
        1. **Install Ollama** (if not already installed):
           - Download from: https://ollama.ai
           - Run: `ollama pull llama2` or `ollama pull mistral`
        
        2. **Configure Pinecone**:
           - Create a `.env` file based on `.env.example`
           - Add your Pinecone API key and environment
        
        3. **Upload Documents**:
           - Use the sidebar to upload PDF or DOCX files
           - Click "Process Documents"
        
        4. **Start Chatting**:
           - Ask questions about your documents
           - Get AI-powered answers with source citations
        
        ### 🔥 Features:
        - ✅ Local LLM (No API costs, unlimited queries)
        - ✅ PDF and DOCX support
        - ✅ Conversational memory
        - ✅ Source document citations
        - ✅ Vector-based retrieval
        """)


if __name__ == "__main__":
    main()
