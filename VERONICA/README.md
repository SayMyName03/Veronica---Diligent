# AI Assistant - NoteMate 🤖

A Jarvis-like AI assistant that can process PDF and DOCX documents and answer questions about their content using LangChain, Pinecone, and a local LLM (Ollama).

## Features

- 📄 **Document Processing**: Upload and process PDF and DOCX files
- 🧠 **Local LLM**: Uses Ollama for unlimited, cost-free AI interactions
- 💾 **Vector Storage**: Pinecone for efficient document retrieval
- 💬 **Conversational AI**: Maintains context across multiple questions
- 📚 **Source Citations**: Shows which parts of documents were used to answer
- 🚀 **No Token Limits**: Run unlimited queries with local LLM

## Tech Stack

- **LangChain**: Document processing and conversational chains
- **Pinecone**: Vector database for document embeddings
- **Ollama**: Local LLM (Llama 2, Mistral, etc.)
- **Streamlit**: Web interface
- **HuggingFace**: Embeddings model

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Download from [https://ollama.ai](https://ollama.ai)
3. **Pinecone Account** - Sign up at [https://www.pinecone.io](https://www.pinecone.io)

## Installation

### Step 1: Install Ollama

```powershell
# Download and install Ollama from https://ollama.ai
# Then pull a model (choose one):
ollama pull llama2
# or
ollama pull mistral
```

### Step 2: Set Up Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your Pinecone credentials:
   ```
   PINECONE_API_KEY=your_actual_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   PINECONE_INDEX_NAME=notemate-index
   OLLAMA_MODEL=llama2
   ```

## Usage

### Start the Application

```powershell
# Make sure Ollama is running (it should auto-start)

# Run the Streamlit app
streamlit run app.py
```

### Using the Application

1. **Upload Documents**: 
   - Click "Browse files" in the sidebar
   - Select one or more PDF or DOCX files
   - Click "Process Documents"

2. **Ask Questions**:
   - Type your question in the chat input
   - The AI will answer based on your documents
   - View source citations to see where the answer came from

3. **Manage Conversation**:
   - Use "Reset Conversation" to start fresh
   - Test LLM connection to verify Ollama is running

## Project Structure

```
VERONICA/
├── app.py                  # Streamlit web interface
├── document_processor.py   # PDF/DOCX processing
├── vector_store.py         # Pinecone vector store manager
├── llm_manager.py          # Ollama LLM integration
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your actual environment variables (not in git)
├── .gitignore            # Git ignore rules
└── uploads/              # Uploaded documents (created automatically)
```

## How It Works

1. **Document Upload**: User uploads PDF/DOCX files
2. **Text Extraction**: Extract text from documents
3. **Chunking**: Split text into manageable chunks (1000 chars with 200 overlap)
4. **Embeddings**: Convert chunks to vector embeddings using HuggingFace
5. **Vector Storage**: Store embeddings in Pinecone
6. **Query Processing**: 
   - User asks a question
   - Question is converted to embedding
   - Similar document chunks are retrieved
   - LLM generates answer using retrieved context
7. **Response**: Display answer with source citations

## Configuration Options

Edit `config.py` to customize:

- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `EMBEDDING_MODEL`: HuggingFace model for embeddings
- `OLLAMA_MODEL`: Which Ollama model to use (llama2, mistral, etc.)

## Available Ollama Models

```powershell
# List available models
ollama list

# Pull additional models
ollama pull mistral
ollama pull codellama
ollama pull llama2:13b
```

## Troubleshooting

### Ollama Connection Error
```powershell
# Check if Ollama is running
ollama list

# Restart Ollama
ollama serve
```

### Pinecone Connection Error
- Verify API key in `.env`
- Check Pinecone environment region
- Ensure index exists or let the app create it

### Memory Issues
- Reduce `CHUNK_SIZE` in `config.py`
- Use a smaller Ollama model (llama2:7b instead of llama2:13b)

## Advanced Usage

### Using Different LLM Models

Edit `.env`:
```
OLLAMA_MODEL=mistral  # or codellama, llama2:13b, etc.
```

### Adjusting Retrieval Settings

In `vector_store.py`, modify the `get_retriever()` method:
```python
return self.vectorstore.as_retriever(search_kwargs={"k": 6})  # Retrieve more chunks
```

### Custom Prompts

Edit the prompt template in `llm_manager.py` to change how the AI responds.

## Performance Tips

1. **Local LLM Speed**: Larger models are slower but more accurate
2. **Chunk Size**: Smaller chunks = more precise but may miss context
3. **Retrieval Count**: More chunks = better context but slower responses
4. **GPU**: If available, Ollama will automatically use it for faster inference

## License

MIT License - feel free to use for your assignment!

## Support

For issues or questions:
1. Check Ollama docs: https://github.com/ollama/ollama
2. Check LangChain docs: https://python.langchain.com/
3. Check Pinecone docs: https://docs.pinecone.io/

---

Built with ❤️ for your AI assignment
