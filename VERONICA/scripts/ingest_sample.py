"""
Programmatic ingest script

Usage (PowerShell):
    python scripts\ingest_sample.py --file sample_document.md

What it does:
- Loads .env
- Reads the given file (supports .pdf, .docx, .doc via DocumentProcessor; falls back to raw text for .md/.txt)
- Splits into chunks using the project's `DocumentProcessor` splitter
- Creates LangChain Document objects and upserts them into Pinecone via `VectorStoreManager`

Note: Run this with your virtual environment active so dependencies (langchain, pinecone, sentence-transformers) are available.
"""
import os
import argparse
from dotenv import load_dotenv

# Ensure we can import project modules (script lives in VERONICA/scripts)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from config import Config
from langchain.schema import Document as LangchainDocument


def parse_args():
    p = argparse.ArgumentParser(description="Ingest a document and upsert embeddings into Pinecone")
    p.add_argument("--file", "-f", default="sample_document.md", help="Path to file to ingest (relative to project root or absolute)")
    return p.parse_args()


def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    # Load environment
    load_dotenv()

    args = parse_args()

    Config.validate()

    file_path = args.file
    if not os.path.isabs(file_path):
        file_path = os.path.join(PROJECT_ROOT, file_path)
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        print(f"Error: file not found: {file_path}")
        return

    print(f"Ingesting: {file_path}")

    processor = DocumentProcessor()

    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".pdf", ".docx", ".doc"]:
        documents = processor.process_document(file_path)
    else:
        # fallback to reading as plain text
        text = load_text_file(file_path)
        metadata = {"source": os.path.basename(file_path), "file_type": ext}
        chunks = processor.text_splitter.split_text(text)
        documents = [LangchainDocument(page_content=chunk, metadata=metadata) for chunk in chunks]

    print(f"Generated {len(documents)} document chunks")

    # Initialize vector store and add documents
    vsm = VectorStoreManager()

    try:
        vsm.add_documents(documents)
        print("Upsert to vector store completed.")
    except Exception as e:
        print(f"Error upserting documents: {e}")


if __name__ == "__main__":
    main()
