import os
from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # sentence-transformers returns a numpy array, convert to list
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
        
    def embed_query(self, query: str) -> list[float]:
        embedding = self.model.encode(query)
        return embedding.tolist()
