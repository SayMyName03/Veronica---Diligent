# Quick Start Guide 🚀

## Step-by-Step Setup

### 1. Install Ollama (Local LLM)

**Download & Install:**
- Visit: https://ollama.ai
- Download for Windows
- Install and it will auto-start

**Pull a Model:**
```powershell
# Choose one of these models:
ollama pull llama2        # 3.8GB - Good balance
ollama pull mistral       # 4.1GB - Better quality
ollama pull llama2:7b     # Smaller, faster
```

### 2. Get Pinecone API Key

1. Go to https://www.pinecone.io
2. Sign up for free account
3. Create a new project
4. Go to "API Keys" section
5. Copy your API key and environment (e.g., `us-west1-gcp`)

### 3. Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env with notepad
notepad .env
```

Add your credentials:
```
PINECONE_API_KEY=your_api_key_here
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=notemate-index
OLLAMA_MODEL=llama2
```

### 5. Test Setup

```powershell
# Make sure virtual environment is activated
python test_setup.py
```

### 6. Run the App

```powershell
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Time Usage

1. **Upload Documents:**
   - Click "Browse files" in sidebar
   - Select PDF or DOCX files
   - Click "Process Documents"
   - Wait for processing to complete

2. **Ask Questions:**
   - Type question in chat box
   - Press Enter
   - View answer with sources

3. **Tips:**
   - Upload multiple documents at once
   - Ask specific questions for better answers
   - Use "Reset Conversation" to start fresh

## Troubleshooting

### "Cannot connect to Ollama"
```powershell
# Check if Ollama is running
ollama list

# If not installed, download from https://ollama.ai
```

### "Pinecone connection error"
- Check your API key in `.env`
- Verify environment name matches Pinecone dashboard
- Index will be created automatically on first run

### "Import errors"
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Slow responses
- Use a smaller model: `ollama pull llama2:7b`
- Update `.env`: `OLLAMA_MODEL=llama2:7b`

## System Requirements

- **RAM:** 8GB minimum (16GB recommended)
- **Disk:** 10GB free space (for models)
- **Python:** 3.8 or higher
- **Internet:** Required for Pinecone (vector storage)

## Demo Flow

1. Start with a simple document (PDF or DOCX)
2. Upload and process
3. Ask: "What is this document about?"
4. Ask: "Summarize the main points"
5. Ask specific questions about content

## Why This Setup?

✅ **Local LLM (Ollama):** Unlimited queries, no API costs
✅ **Pinecone:** Fast vector search, free tier available
✅ **LangChain:** Industry-standard RAG framework
✅ **Streamlit:** Beautiful, interactive UI

Perfect for your assignment requirements! 🎓
