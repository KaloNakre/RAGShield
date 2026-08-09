from typing import List
from app.rag.vector_store import VectorStore
from app.schemas.document import RetrievedDocument, DocumentChunk, DocumentMetadata

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> List[RetrievedDocument]:
        raw_results = self.vector_store.search(query, top_k=top_k)
        
        retrieved_docs = []
        for res in raw_results:
            metadata = DocumentMetadata(**res['metadata'])
            chunk = DocumentChunk(
                chunk_id=res['id'],
                document_id=metadata.document_id,
                text=res['text'],
                metadata=metadata
            )
            # Convert distance to relevance (cosine distance: smaller is better, relevance is 1-distance or similar)
            # Assuming distance is cosine distance (0 to 2)
            relevance = max(0.0, 1.0 - (res['distance'] / 2.0))
            
            retrieved_docs.append(RetrievedDocument(
                chunk=chunk,
                relevance_score=relevance
            ))
            
        return retrieved_docs
