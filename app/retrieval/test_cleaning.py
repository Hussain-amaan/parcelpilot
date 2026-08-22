from app.retrieval.pdf_loader import load_all_pdfs
from app.retrieval.text_processing import clean_text


documents = load_all_pdfs()

for document in documents:

    cleaned = clean_text(document["text"])

    print("=" * 70)
    print(document["filename"])
    print("=" * 70)

    print(cleaned[:1000])
    print()