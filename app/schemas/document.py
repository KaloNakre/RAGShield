from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    classification: str = "public"
    owner: str = "system"
    access_level: str = "public"
    
class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    metadata: DocumentMetadata
    
class RetrievedDocument(BaseModel):
    chunk: DocumentChunk
    relevance_score: float
