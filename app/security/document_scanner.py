from app.schemas.security import SecurityDecision
from app.schemas.document import RetrievedDocument
from typing import List

class DocumentScanner:
    def __init__(self):
        self.indirect_injection_keywords = [
            "ignore the user",
            "ignore all security policies",
            "reveal confidential",
            "new instruction:"
        ]

    def scan_documents(self, documents: List[RetrievedDocument]) -> List[RetrievedDocument]:
        safe_docs = []
        for doc in documents:
            is_safe = True
            lower_text = doc.chunk.text.lower()
            for keyword in self.indirect_injection_keywords:
                if keyword in lower_text:
                    is_safe = False
                    break
            
            if is_safe:
                safe_docs.append(doc)
                
        return safe_docs
