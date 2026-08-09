from app.security.access_control import AccessControl
from app.schemas.document import RetrievedDocument, DocumentChunk, DocumentMetadata

def test_guest_access():
    ac = AccessControl()
    
    meta_pub = DocumentMetadata(document_id="1", filename="pub.txt", classification="public", access_level="public")
    doc_pub = RetrievedDocument(chunk=DocumentChunk(chunk_id="1", document_id="1", text="text", metadata=meta_pub), relevance_score=0.9)
    
    meta_conf = DocumentMetadata(document_id="2", filename="conf.txt", classification="confidential", access_level="confidential")
    doc_conf = RetrievedDocument(chunk=DocumentChunk(chunk_id="2", document_id="2", text="text", metadata=meta_conf), relevance_score=0.9)
    
    filtered = ac.filter_documents([doc_pub, doc_conf], "guest")
    assert len(filtered) == 1
    assert filtered[0].chunk.metadata.filename == "pub.txt"

def test_admin_access():
    ac = AccessControl()
    
    meta_pub = DocumentMetadata(document_id="1", filename="pub.txt", classification="public", access_level="public")
    doc_pub = RetrievedDocument(chunk=DocumentChunk(chunk_id="1", document_id="1", text="text", metadata=meta_pub), relevance_score=0.9)
    
    meta_conf = DocumentMetadata(document_id="2", filename="conf.txt", classification="confidential", access_level="confidential")
    doc_conf = RetrievedDocument(chunk=DocumentChunk(chunk_id="2", document_id="2", text="text", metadata=meta_conf), relevance_score=0.9)
    
    filtered = ac.filter_documents([doc_pub, doc_conf], "admin")
    assert len(filtered) == 2
