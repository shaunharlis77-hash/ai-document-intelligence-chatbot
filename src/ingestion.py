import os
import json
import streamlit as st

from src.document_processing import (
    extract_text_from_pdf,
    extract_text_from_pdf_bytes,
    extract_text_with_document_intelligence,
    chunk_text,
)

from src.embeddings import get_embedding

from src.cache import (
    load_ingestion_cache,
    save_ingestion_cache,
)

from src.azure_storage import (
    list_blobs_in_container,
    download_blob_to_bytes,
)

from src.azure_search import (
    ensure_search_index_exists,
    upload_chunks_to_search,
)

PDF_FOLDER = "pdfs"
DATA_FOLDER = "data"
OUTPUT_FILE = os.path.join(DATA_FOLDER, "chunks.json")

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

def save_chunks_to_json(all_chunks, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_chunks, file, indent=4, ensure_ascii=False)
        

def load_chunks_from_json(output_file):
    if not os.path.exists(output_file):
        return []

    with open(output_file, "r", encoding="utf-8") as file:
        return json.load(file)
    
def process_pdfs(pages_to_process=None, pages_param=None, selected_files=None):
    cache = load_ingestion_cache()

    if selected_files is not None:
        pdf_files = [file for file in selected_files if file.lower().endswith(".pdf")]
    else:
        pdf_files = [file for file in os.listdir(PDF_FOLDER) if file.lower().endswith(".pdf")]
    if not pdf_files:
        return 0, "No PDF files found in the pdfs folder.", [], [], []

    all_chunks = []
    di_used_files = []
    fallback_used_files = []
    di_failed_files = []
    cached_reused_files = []
    newly_processed_files = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        last_modified = os.path.getmtime(pdf_path)
        cached_file = cache.get(pdf_file)
        is_unchanged = (
            cached_file is not None and
            cached_file.get("last_modified") == last_modified and
            cached_file.get("pages_param") == pages_param
        )

        if is_unchanged:
            st.info(f"{pdf_file} is unchanged. Reusing cached chunks and skipping reprocessing.")
            cached_reused_files.append(pdf_file)
            cached_chunks = cached_file.get("chunks", [])
            all_chunks.extend(cached_chunks)
            continue
        else:
            st.info(f"{pdf_file} is new or changed. Processing.")
            newly_processed_files.append(pdf_file)

        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
        except Exception as e:
            st.error(f"Error reading local PDF '{pdf_file}': {e}")
            continue

        extracted_text, used_di = extract_text_with_document_intelligence(pdf_bytes, pages_param=pages_param)

        if used_di and extracted_text.strip():
            di_used_files.append(pdf_file)
        else:
            di_failed_files.append(pdf_file)
            extracted_text = extract_text_from_pdf(pdf_path, max_pages=pages_to_process)

            if extracted_text.strip():
                fallback_used_files.append(pdf_file)

        if extracted_text.strip():
            chunks = chunk_text(extracted_text, chunk_size=140, overlap=40)
            file_base = os.path.splitext(pdf_file)[0]
            file_chunks = []

            for i, chunk in enumerate(chunks, start=1):
                embedding = get_embedding(chunk)

                if embedding is None:
                    continue

                chunk_record = {
                    "id": f"{file_base}_{i}".replace(" ", "_"),
                    "source_file": pdf_file,
                    "chunk_number": i,
                    "content": chunk,
                    "embedding": embedding
                }
                all_chunks.append(chunk_record)
                file_chunks.append(chunk_record)

        cache[pdf_file] = {
            "last_modified": last_modified,
            "pages_param": pages_param,
            "chunks": file_chunks if extracted_text.strip() else []
        }

    save_chunks_to_json(all_chunks, OUTPUT_FILE)
    save_ingestion_cache(cache)
    return (
        len(all_chunks),
        "Local PDF ingestion completed.",
        di_used_files,
        fallback_used_files,
        di_failed_files,
        cached_reused_files,
        newly_processed_files
    )


def process_pdfs_from_azure(pages_to_process=None, pages_param=None):
    blob_names = list_blobs_in_container()

    if not blob_names:
        return 0, "No PDF blobs found in Azure Storage.", [], [], []

    all_chunks = []
    di_used_files = []
    fallback_used_files = []
    di_failed_files = []
    

    for blob_name in blob_names:
        if not blob_name.lower().endswith(".pdf"):
            continue

        pdf_bytes = download_blob_to_bytes(blob_name)

        if pdf_bytes is None:
            continue

        extracted_text, used_di = extract_text_with_document_intelligence(pdf_bytes, pages_param=pages_param)

        if used_di and extracted_text.strip():
            di_used_files.append(blob_name)
        else:
            di_failed_files.append(blob_name)
            extracted_text = extract_text_from_pdf_bytes(pdf_bytes, max_pages=pages_to_process)

            if extracted_text.strip():
                fallback_used_files.append(blob_name)

        if extracted_text.strip():
            chunks = chunk_text(extracted_text, chunk_size=140, overlap=40)
            file_base = os.path.splitext(blob_name)[0]

            for i, chunk in enumerate(chunks, start=1):
                embedding = get_embedding(chunk)

                if embedding is None:
                    continue

                chunk_record = {
                    "id": f"{file_base}_{i}".replace(" ", "_"),
                    "source_file": blob_name,
                    "chunk_number": i,
                    "content": chunk,
                    "embedding": embedding
                }
                all_chunks.append(chunk_record)

    save_chunks_to_json(all_chunks, OUTPUT_FILE)

    if ensure_search_index_exists():
        upload_chunks_to_search(all_chunks)

    return (
        len(all_chunks),
        "Azure PDF ingestion completed.",
        di_used_files,
        fallback_used_files,
        di_failed_files
)
