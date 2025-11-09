# Assignment Guide: Building Your AI Assistant 📚

## Overview

This project fulfills all your assignment requirements:

✅ **LangChain** - For document processing and conversational AI  
✅ **Pinecone** - For vector storage and semantic search  
✅ **Local LLM** - Ollama (unlimited queries, no token limits)  
✅ **PDF/DOCX Support** - Upload and process documents  
✅ **Conversational Interface** - Chat with your documents  

## Architecture Diagram

```
┌─────────────┐
│  User       │
│  Uploads    │
│  PDF/DOCX   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Document Processor  │ ← Extracts text, splits into chunks
│ (LangChain)         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Embedding Model     │ ← Converts text to vectors
│ (HuggingFace)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Vector Store        │ ← Stores document embeddings
│ (Pinecone)          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ User asks question  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Retriever           │ ← Finds relevant chunks
│ (Similarity Search) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Local LLM           │ ← Generates answer
│ (Ollama/Llama2)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Answer with Sources │
└─────────────────────┘
```

## Key Components Explained

### 1. Document Processing (`document_processor.py`)
- **Purpose**: Extract text from PDF and DOCX files
- **How**: Uses PyPDF for PDFs, python-docx for DOCX files
- **Output**: Splits documents into chunks (1000 chars with 200 overlap)
- **Why chunks?**: Smaller pieces are easier to search and fit in LLM context

### 2. Vector Store (`vector_store.py`)
- **Purpose**: Store and retrieve document embeddings
- **How**: Converts text to vectors using HuggingFace embeddings
- **Storage**: Pinecone cloud vector database
- **Benefit**: Fast semantic search (finds similar meaning, not just keywords)

### 3. LLM Manager (`llm_manager.py`)
- **Purpose**: Handle conversations with local LLM
- **How**: Uses Ollama to run Llama 2 or Mistral locally
- **Memory**: Maintains conversation context
- **Advantage**: Unlimited queries, no API costs

### 4. Streamlit App (`app.py`)
- **Purpose**: User interface
- **Features**: 
  - Document upload
  - Chat interface
  - Source citations
  - Conversation management

## How RAG (Retrieval-Augmented Generation) Works

This project uses RAG, a technique that combines:

1. **Retrieval**: Finding relevant information from documents
2. **Augmentation**: Adding that information to the prompt
3. **Generation**: LLM creates answer based on retrieved context

**Example Flow:**
```
User: "What are the types of AI?"
         ↓
1. Convert question to vector
2. Search Pinecone for similar chunks
3. Retrieve top 4 most relevant chunks
4. Send to LLM: "Based on this context: [chunks], answer: [question]"
5. LLM generates answer using provided context
6. Display answer + show source documents
```

## Why This Tech Stack?

### LangChain
- Industry standard for LLM applications
- Pre-built chains for common tasks
- Easy document processing
- Memory management

### Pinecone
- Cloud-hosted (no local setup needed)
- Fast vector similarity search
- Free tier available
- Scalable

### Ollama (Local LLM)
- **No API costs** - Run unlimited queries
- **Privacy** - Data stays on your machine
- **Fast** - No network latency
- **Multiple models** - llama2, mistral, codellama, etc.

## Installation Steps (Detailed)

### Step 1: Install Ollama

**Why first?** Ollama is the largest download and takes time to set up.

1. Go to https://ollama.ai
2. Download Windows installer
3. Run installer (it will add to PATH)
4. Open PowerShell and run:
   ```powershell
   ollama pull llama2
   ```
   This downloads the Llama 2 model (~3.8GB)

**Model Options:**
- `llama2` - 3.8GB, good quality
- `mistral` - 4.1GB, better quality
- `llama2:7b` - Smaller, faster
- `llama2:13b` - Larger, better quality

### Step 2: Get Pinecone Credentials

1. Go to https://www.pinecone.io
2. Sign up (free tier available)
3. Create a project
4. Go to "API Keys"
5. Copy:
   - API Key
   - Environment (e.g., `us-west1-gcp`)

### Step 3: Python Setup

```powershell
# Navigate to project
cd "c:\Users\saymy\OneDrive\Desktop\Diligent\VERONICA"

# Run setup script
.\setup.ps1

# Or manually:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 4: Configure Environment

Edit `.env` file:
```
PINECONE_API_KEY=pcsk_xxxxx_xxxxxxxxxxxxx
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=notemate-index
OLLAMA_MODEL=llama2
```

### Step 5: Test Everything

```powershell
python test_setup.py
```

This checks:
- Configuration loaded
- Ollama running
- Pinecone connected
- Dependencies installed

### Step 6: Run Application

```powershell
streamlit run app.py
```

Browser opens at `http://localhost:8501`

## Usage Demo

### 1. Upload Documents

- Click "Browse files" in sidebar
- Select PDF or DOCX files (can select multiple)
- Click "Process Documents"
- Wait for "Successfully processed X documents!" message

### 2. Test Connection

- Click "Test LLM Connection" in sidebar
- Should show "✅ Ollama is running!"
- If not, make sure Ollama is installed and running

### 3. Ask Questions

Start with simple questions:
- "What is this document about?"
- "Summarize the main points"
- "What are the key topics covered?"

Then ask specific questions:
- "Explain [specific topic] in detail"
- "What does the document say about [topic]?"
- "Compare [topic A] and [topic B]"

### 4. View Sources

- Click "Source Documents" expander under answers
- See which parts of documents were used
- Verify answer accuracy

## Testing Your Assignment

Use the included `sample_document.md` to test:

1. **Convert to PDF** (if needed):
   - Open in Word/browser
   - Save/Print as PDF

2. **Upload and Process**

3. **Ask Test Questions**:
   - "What are the three types of AI?"
   - "How is AI used in healthcare?"
   - "What are the ethical considerations?"
   - "What is the difference between machine learning and deep learning?"

4. **Verify**:
   - Answers are accurate
   - Sources are cited
   - Conversation maintains context

## Troubleshooting

### "Cannot connect to Ollama"

**Problem**: Ollama not running or not installed

**Solution**:
```powershell
# Check if installed
ollama list

# If not installed, download from https://ollama.ai
# After install, pull a model
ollama pull llama2
```

### "Pinecone connection error"

**Problem**: Invalid API key or environment

**Solution**:
- Check `.env` file has correct values
- Verify API key from Pinecone dashboard
- Check environment name matches (e.g., `us-west1-gcp`)

### "Import errors" in Python

**Problem**: Dependencies not installed

**Solution**:
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall
pip install -r requirements.txt --upgrade
```

### Slow responses

**Problem**: Large model or limited hardware

**Solution**:
```powershell
# Use smaller model
ollama pull llama2:7b

# Update .env
# OLLAMA_MODEL=llama2:7b
```

### Out of memory errors

**Problem**: Not enough RAM

**Solution**:
- Use smaller model (llama2:7b)
- Reduce chunk size in `config.py`
- Close other applications

## Assignment Demonstration Tips

### What to Show

1. **Document Upload**
   - Upload PDF/DOCX
   - Show processing happens

2. **Questioning**
   - Ask diverse questions
   - Show accurate answers
   - Demonstrate source citations

3. **Conversation Memory**
   - Ask follow-up questions
   - Show context is maintained

4. **Technical Stack**
   - Mention LangChain for processing
   - Highlight Pinecone for vectors
   - Emphasize local LLM (unlimited queries)

### What to Explain

1. **RAG Architecture**
   - Document → Chunks → Vectors → Storage
   - Query → Retrieve → Generate answer

2. **Why Local LLM**
   - No API costs
   - Unlimited queries (meets assignment requirement)
   - Privacy

3. **Vector Search Benefits**
   - Semantic understanding
   - Not just keyword matching
   - Fast retrieval

## Extension Ideas

If you want to go beyond basic requirements:

1. **Multiple Document Types**
   - Add support for TXT, CSV
   - Web page scraping

2. **Better UI**
   - Custom Streamlit theme
   - Document management (delete, view)

3. **Advanced Features**
   - Chat history export
   - Document summarization
   - Keyword extraction

4. **Performance**
   - Caching responses
   - Async processing
   - Progress bars

## Code Structure for Report

If writing a report, explain these files:

- `config.py` - Configuration management
- `document_processor.py` - PDF/DOCX handling
- `vector_store.py` - Pinecone integration
- `llm_manager.py` - Ollama/LLM handling
- `app.py` - Streamlit UI

## Key Concepts to Mention

1. **Embeddings**: Converting text to numerical vectors
2. **Vector Search**: Finding similar content by vector proximity
3. **Chunking**: Breaking documents into manageable pieces
4. **RAG**: Retrieval-Augmented Generation
5. **Conversational Memory**: Maintaining chat context

## Performance Metrics

Track these for your report:
- Document processing time
- Query response time
- Chunk size vs accuracy
- Number of documents supported

## Conclusion

This project demonstrates:
✅ Document processing (PDF, DOCX)
✅ Vector embeddings and storage (Pinecone)
✅ Local LLM integration (Ollama)
✅ Conversational AI (LangChain)
✅ Unlimited queries (no token limits)

All assignment requirements met! 🎯

## Resources

- **LangChain**: https://python.langchain.com/
- **Pinecone**: https://docs.pinecone.io/
- **Ollama**: https://github.com/ollama/ollama
- **Streamlit**: https://docs.streamlit.io/

Good luck with your assignment! 🚀
