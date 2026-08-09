import chromadb
from chromadb.config import Settings
import os
import uuid
from typing import List, Dict, Any

from app.schemas.document import DocumentChunk, DocumentMetadata
from app.rag.embeddings import Embeddings

class VectorStore:
    def __init__(self, persist_directory: str = "./data/chroma"):
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="ragshield_docs",
            metadata={"hnsw:space": "cosine"}
        )
        self.embeddings = Embeddings()

    def add_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            return
            
        texts = [chunk.text for chunk in chunks]
        ids = [chunk.chunk_id for chunk in chunks]
        metadatas = [chunk.metadata.model_dump() for chunk in chunks]
        
        embeddings = self.embeddings.embed_texts(texts)
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embeddings.embed_query(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved = []
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = {
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results and results['distances'] else 0.0
                }
                retrieved.append(doc)
                
        return retrieved
