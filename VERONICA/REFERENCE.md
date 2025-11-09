# Quick Reference Card 📋

## Commands Cheat Sheet

### Setup (One-time)
```powershell
# Run automated setup
.\setup.ps1

# Or manually:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Ollama Commands
```powershell
# List installed models
ollama list

# Pull a model
ollama pull llama2
ollama pull mistral

# Remove a model
ollama rm llama2

# Check if running
ollama list
```

### Running the App
```powershell
# Activate environment (if not active)
.\venv\Scripts\Activate.ps1

# Test setup
python test_setup.py

# Test Ollama only
python test_ollama.py

# Run the app
streamlit run app.py
```

### Common Issues

| Problem | Solution |
|---------|----------|
| "Ollama not found" | Install from https://ollama.ai |
| "No module named X" | `pip install -r requirements.txt` |
| "Pinecone error" | Check API key in `.env` |
| "Slow responses" | Use smaller model: `ollama pull llama2:7b` |
| "Out of memory" | Close other apps, use smaller model |

## File Structure

```
VERONICA/
├── app.py                  # Main Streamlit app (RUN THIS)
├── config.py               # Settings
├── document_processor.py   # PDF/DOCX handler
├── vector_store.py         # Pinecone integration
├── llm_manager.py          # Ollama/LLM handler
├── test_setup.py           # System checker
├── test_ollama.py          # Ollama checker
├── requirements.txt        # Dependencies
├── .env                    # Your credentials (EDIT THIS)
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
├── ASSIGNMENT_GUIDE.md    # Assignment help
└── sample_document.md     # Test document
```

## Environment Variables (.env)

```bash
# Required for Pinecone
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=us-west1-gcp

# Optional (has defaults)
PINECONE_INDEX_NAME=notemate-index
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

## Workflow

1. **Setup** (once)
   - Install Ollama → Pull model → Configure .env → Install dependencies

2. **Run** (every time)
   - Activate venv → Run app → Upload docs → Ask questions

3. **Test** (if issues)
   - Run test_setup.py → Check Ollama → Check Pinecone

## Model Comparison

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama2:7b | 3.8GB | Fast | Good | Testing, limited RAM |
| llama2 (13b) | 7.4GB | Medium | Better | Production |
| mistral | 4.1GB | Medium | Best | Best quality |
| codellama | 3.8GB | Fast | Good | Code-related docs |

## URLs

- **App**: http://localhost:8501
- **Ollama**: http://localhost:11434
- **Ollama Download**: https://ollama.ai
- **Pinecone**: https://www.pinecone.io

## Tips

✅ **Do:**
- Use specific questions
- Upload multiple related documents
- Check source citations
- Reset conversation when switching topics

❌ **Don't:**
- Ask questions before uploading docs
- Expect answers outside document content
- Upload too many large files at once (start small)

## Performance Tips

- **Faster responses**: Use llama2:7b
- **Better quality**: Use mistral
- **Less memory**: Reduce CHUNK_SIZE in config.py
- **More context**: Increase k in vector_store.py

## Demo Script

1. Upload sample_document.md (as PDF)
2. Ask: "What are the three types of AI?"
3. Ask: "How is AI used in healthcare?"
4. Ask: "What did you just tell me?" (show memory)
5. View source citations

---

**Need help?** Check ASSIGNMENT_GUIDE.md for detailed explanations!
