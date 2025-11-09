from dotenv import load_dotenv
import os
import pinecone

# Resolve project root and .env path reliably even when script is run from different cwd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    # Fall back to default load (current working directory)
    load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY", "")
ENV = os.getenv("PINECONE_ENVIRONMENT", "")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "")

if not API_KEY or not ENV:
    print(f"Tried .env path: {ENV_PATH}")
    print("Current working directory:", os.getcwd())
    print("Environment variables loaded (partial):")
    print("  PINECONE_API_KEY=", bool(os.getenv("PINECONE_API_KEY")))
    print("  PINECONE_ENVIRONMENT=", bool(os.getenv("PINECONE_ENVIRONMENT")))
    raise SystemExit("Set PINECONE_API_KEY and PINECONE_ENVIRONMENT in .env (check path)")

pinecone.init(api_key=API_KEY, environment=ENV)
if not INDEX_NAME:
    print("Set PINECONE_INDEX_NAME in .env to see stats for a specific index.")
else:
    idx = pinecone.Index(INDEX_NAME)
    print("Index stats:", idx.describe_index_stats())