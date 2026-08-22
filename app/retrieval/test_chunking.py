from app.retrieval.pdf_loader import load_all_pdfs
from app.retrieval.text_processing import clean_text
from app.retrieval.chunker import chunk_text


documents = load_all_pdfs()

for document in documents:

    cleaned_text = clean_text(document["text"])

    chunks = chunk_text(cleaned_text)

    print("=" * 70)
    print(document["filename"])
    print(f"Number of chunks: {len(chunks)}")
    print("=" * 70)

    for i, chunk in enumerate(chunks, start=1):

        print(f"\n--- CHUNK {i} ---")
        print(chunk[:1000])

    print()