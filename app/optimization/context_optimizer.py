from typing import List, Tuple
from app.schemas.document import RetrievedDocument
from app.optimization.token_counter import TokenCounter

class ContextOptimizer:
    def __init__(self, max_context_tokens: int = 2000):
        self.max_context_tokens = max_context_tokens
        self.token_counter = TokenCounter()

    def optimize_context(self, documents: List[RetrievedDocument]) -> Tuple[List[RetrievedDocument], int, int]:
        # 1. Remove exact duplicates
        unique_docs = []
        seen_texts = set()
        for doc in documents:
            if doc.chunk.text not in seen_texts:
                seen_texts.add(doc.chunk.text)
                unique_docs.append(doc)

        # 2. Rank by relevance
        ranked_docs = sorted(unique_docs, key=lambda x: x.relevance_score, reverse=True)

        original_tokens = sum(self.token_counter.count_tokens(doc.chunk.text) for doc in documents)
        
        optimized_docs = []
        current_tokens = 0
        
        # 3. Context Length Check & Trim Low-Value Content
        for doc in ranked_docs:
            doc_tokens = self.token_counter.count_tokens(doc.chunk.text)
            if current_tokens + doc_tokens > self.max_context_tokens:
                remaining_tokens = self.max_context_tokens - current_tokens
                if remaining_tokens > 50:
                    allowed_chars = remaining_tokens * self.token_counter.chars_per_token
                    doc.chunk.text = doc.chunk.text[:allowed_chars] + "..."
                    optimized_docs.append(doc)
                    current_tokens += remaining_tokens
                break
            else:
                optimized_docs.append(doc)
                current_tokens += doc_tokens
                
        optimized_tokens = current_tokens
        return optimized_docs, original_tokens, optimized_tokens
