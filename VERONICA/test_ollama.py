"""
Quick test to verify Ollama is working
"""
import requests

def test_ollama():
    """Test if Ollama is accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("✓ Ollama is running!")
            models = response.json().get("models", [])
            if models:
                print("\nInstalled models:")
                for model in models:
                    print(f"  - {model['name']}")
            else:
                print("\n⚠ No models installed yet")
                print("  Run: ollama pull llama2")
            return True
        else:
            print("✗ Ollama returned error")
            return False
    except Exception as e:
        print("✗ Cannot connect to Ollama")
        print(f"  Error: {str(e)}")
        print("\n  Make sure Ollama is installed and running:")
        print("  1. Download from https://ollama.ai")
        print("  2. Install and run")
        print("  3. Pull a model: ollama pull llama2")
        return False

if __name__ == "__main__":
    print("Testing Ollama connection...\n")
    test_ollama()
