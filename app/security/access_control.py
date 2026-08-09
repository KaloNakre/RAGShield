from typing import List
from app.schemas.document import RetrievedDocument

class AccessControl:
    def __init__(self):
        # In a real app, this would be a proper RBAC/ABAC system
        self.role_permissions = {
            "guest": ["public"],
            "employee": ["public", "internal"],
            "admin": ["public", "internal", "confidential", "restricted"]
        }

    def filter_documents(self, documents: List[RetrievedDocument], user_role: str) -> List[RetrievedDocument]:
        allowed_levels = self.role_permissions.get(user_role, ["public"])
        
        filtered_docs = []
        for doc in documents:
            if doc.chunk.metadata.access_level in allowed_levels:
                filtered_docs.append(doc)
                
        return filtered_docs
