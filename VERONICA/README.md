# VERONICA 🤖 – Local Document Q&A Assistant

VERONICA is a local, privacy-first AI assistant that answers questions about your own documents (PDF/DOCX). It runs a local LLM via Ollama and uses Pinecone for fast semantic retrieval.

## Features

- 📄 PDF & DOCX ingestion
- 🧠 Local LLM via Ollama (no API costs)
- 💾 Pinecone vector search for relevant snippets
- 💬 Conversational answers grounded in your docs
- 📚 Source citations for transparency
- � No hardcoded secrets; configure with `.env`

## Tech Stack

- LangChain (document processing + chains)
- Pinecone (vector database)
- Ollama (local LLM)
- Streamlit (UI)
- HuggingFace sentence-transformers (embeddings)

## Prerequisites

1. Python 3.10+ recommended
2. Ollama installed: https://ollama.ai
3. Pinecone account: https://www.pinecone.io

## Installation

### 1) Install Ollama

```powershell
# Download and install Ollama from https://ollama.ai
# Then pull a model (choose one):
ollama pull llama2
# or
ollama pull mistral
```

### 2) Set up Python environment (Windows PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
./.venv/Scripts/Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3) Configure environment variables

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your settings (example):
   ```
   # Pinecone
   PINECONE_API_KEY=your_api_key_here
   PINECONE_ENVIRONMENT=us-east-1
   PINECONE_INDEX_NAME=diligent-33

   # Ollama
   OLLAMA_MODEL=llama2
   OLLAMA_BASE_URL=http://localhost:11434
   ```

Security note: Do NOT commit `.env`. A `.gitignore` is provided.

## Usage

### Start VERONICA

```powershell
# Make sure Ollama is running (it should auto-start)

# Run the Streamlit app
streamlit run app.py
```

### Use the app

1. **Upload Documents**: 
   - Click "Browse files" in the sidebar
   - Select one or more PDF or DOCX files
   - Click "Process Documents" to ingest

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
├── .gitignore             # Git ignore rules (keeps .env out of git)
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

- `CHUNK_SIZE` (default: 1000)
- `CHUNK_OVERLAP` (default: 200)
- `EMBEDDING_MODEL` (default: sentence-transformers/all-MiniLM-L6-v2)
- `OLLAMA_MODEL` (e.g., llama2, mistral)

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

### Use different LLM models

Edit `.env`:
```
OLLAMA_MODEL=mistral  # or codellama, llama2:13b, etc.
```

### Adjust retrieval settings

In `vector_store.py`, modify the `get_retriever()` method:
```python
return self.vectorstore.as_retriever(search_kwargs={"k": 6})  # Retrieve more chunks
```

### Custom prompts

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

Built with ❤️ – VERONICA
