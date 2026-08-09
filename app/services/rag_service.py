from app.rag.loader import DocumentLoader
from app.rag.chunker import TextChunker
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.security.prompt_detector import PromptDetector
from app.security.document_scanner import DocumentScanner
from app.security.access_control import AccessControl
from app.security.risk_engine import RiskEngine
from app.security.output_filter import OutputFilter
from app.optimization.context_optimizer import ContextOptimizer
from app.llm.client import MockLLMClient
from app.schemas.document import DocumentChunk, DocumentMetadata
import uuid
import os

class RAGService:
    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.vector_store = VectorStore()
        self.retriever = Retriever(self.vector_store)
        
        self.prompt_detector = PromptDetector()
        self.doc_scanner = DocumentScanner()
        self.access_control = AccessControl()
        self.risk_engine = RiskEngine()
        self.output_filter = OutputFilter()
        
        self.optimizer = ContextOptimizer()
        self.llm = MockLLMClient()

    def upload_document(self, file_path: str, classification: str, owner: str = "system", access_level: str = "public") -> dict:
        text = self.loader.load_document(file_path)
        chunks_text = self.chunker.chunk_text(text)
        
        doc_id = str(uuid.uuid4())
        filename = os.path.basename(file_path)
        metadata = DocumentMetadata(
            document_id=doc_id,
            filename=filename,
            classification=classification,
            owner=owner,
            access_level=access_level
        )
        
        chunks = []
        for c in chunks_text:
            chunks.append(DocumentChunk(
                chunk_id=str(uuid.uuid4()),
                document_id=doc_id,
                text=c,
                metadata=metadata
            ))
            
        self.vector_store.add_chunks(chunks)
        
        return {
            "filename": filename,
            "chunks": len(chunks),
            "status": "Indexed"
        }

    def process_chat(self, query: str, user_role: str = "guest") -> dict:
        # 1. Input Security
        prompt_sec = self.prompt_detector.analyze_query(query)
        if not prompt_sec.is_allowed:
            return self._build_response(prompt_sec, [], 0, 0, 0, "Query Blocked: " + prompt_sec.reason)

        # 2. Retrieval
        retrieved_docs = self.retriever.retrieve(query)
        
        # 3. Access Control
        allowed_docs = self.access_control.filter_documents(retrieved_docs, user_role)
        
        # 4. Document Security
        safe_docs = self.doc_scanner.scan_documents(allowed_docs)
        
        doc_risk = 0 if len(safe_docs) == len(allowed_docs) else 30
        overall_sec = self.risk_engine.calculate_overall_risk(prompt_sec, doc_risk)
        
        if not overall_sec.is_allowed:
            return self._build_response(overall_sec, [], 0, 0, 0, "Blocked due to high risk.")

        # 5. Token Optimization
        opt_docs, orig_tokens, opt_tokens = self.optimizer.optimize_context(safe_docs)
        tokens_saved = orig_tokens - opt_tokens
        
        # 6. LLM Generation
        context = "\n".join([d.chunk.text for d in opt_docs])
        prompt = f"Context: {context}\nQuery: {query}"
        llm_response = self.llm.generate(prompt)
        
        # 7. Output Security
        if not self.output_filter.is_safe(llm_response):
            return self._build_response(overall_sec, opt_docs, orig_tokens, opt_tokens, tokens_saved, "Response Blocked: The generated response contained restricted information and was blocked by the security layer.")
            
        return self._build_response(overall_sec, opt_docs, orig_tokens, opt_tokens, tokens_saved, llm_response)

    def _build_response(self, sec, docs, orig, opt, saved, answer):
        return {
            "security": {
                "risk_score": sec.risk_score,
                "risk_level": sec.risk_level,
                "decision": "ALLOW" if sec.is_allowed else "BLOCK"
            },
            "retrieval": {
                "documents": len(docs),
                "sources": [{"filename": d.chunk.metadata.filename, "relevance": round(d.relevance_score * 100, 2)} for d in docs]
            },
            "tokens": {
                "original": orig,
                "optimized": opt,
                "saved": saved,
                "reduction": round((saved / orig * 100), 1) if orig > 0 else 0
            },
            "answer": answer
        }
