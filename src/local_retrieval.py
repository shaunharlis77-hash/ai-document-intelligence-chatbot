from src.embeddings import get_embedding, cosine_similarity


def keyword_search(query, chunks):
    query_embedding = get_embedding(query)

    if query_embedding is None:
        return []

    scored_chunks = []

    for chunk in chunks:
        chunk_embedding = chunk.get("embedding")

        if not chunk_embedding:
            continue

        score = cosine_similarity(query_embedding, chunk_embedding)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return scored_chunks