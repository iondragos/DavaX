from .embeddings import get_embedding

def semantic_retriever(query: str, collection, top_k: int = 3):
    embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results["documents"][0], results["metadatas"][0]
