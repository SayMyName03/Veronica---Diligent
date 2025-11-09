# Setup script for AI Assistant
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "AI Assistant - Setup Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check Ollama
Write-Host ""
Write-Host "Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaCheck = ollama list 2>&1
    Write-Host "✓ Ollama is installed" -ForegroundColor Green
    
    # Check for models
    if ($ollamaCheck -match "llama2|mistral") {
        Write-Host "✓ LLM model found" -ForegroundColor Green
    } else {
        Write-Host "⚠ No LLM model found" -ForegroundColor Yellow
        Write-Host "  Run: ollama pull llama2" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Ollama not found" -ForegroundColor Red
    Write-Host "  Download from: https://ollama.ai" -ForegroundColor Gray
}

# Check .env configuration
Write-Host ""
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    if ($envContent -match "PINECONE_API_KEY=\w+") {
        Write-Host "✓ Pinecone configured" -ForegroundColor Green
    } else {
        Write-Host "⚠ Pinecone not configured" -ForegroundColor Yellow
        Write-Host "  Edit .env and add your Pinecone API key" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠ .env file not found" -ForegroundColor Yellow
}

# Final instructions
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure .env file with your Pinecone API key"
Write-Host "2. Install Ollama from https://ollama.ai (if not installed)"
Write-Host "3. Run: ollama pull llama2"
Write-Host "4. Test setup: python test_setup.py"
Write-Host "5. Start app: streamlit run app.py"
Write-Host ""
Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Gray
Write-Host ""
