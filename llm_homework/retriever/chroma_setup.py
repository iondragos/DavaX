from chromadb import PersistentClient

def get_chroma_collection(path: str = "./chroma_store", name: str = "book_summaries"):
    chroma_client = PersistentClient(path=path)
    return chroma_client.get_or_create_collection(name=name)
