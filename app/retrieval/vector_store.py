from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.retrieval.document_processor import process_documents


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"


# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def create_vector_store():
    """
    Create the ChromaDB vector store and add
    all processed document chunks.
    """

    # Create Chroma directory
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    # Chroma persistent client
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Create/reset collection
    collection = client.get_or_create_collection(
        name="parcelpilot_documents"
    )

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Process PDF documents
    documents = process_documents()

    texts = [
        document["text"]
        for document in documents
    ]

    metadatas = [
        document["metadata"]
        for document in documents
    ]

    ids = [
        f"{metadata['source']}_chunk_{metadata['chunk_id']}"
        for metadata in metadatas
    ]

    # Generate embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    ).tolist()

    # Add documents to ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("\nVector store created successfully!")
    print(f"Documents/chunks: {len(texts)}")
    print(f"Location: {CHROMA_DIR}")


if __name__ == "__main__":
    create_vector_store()