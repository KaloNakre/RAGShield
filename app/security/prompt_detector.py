from app.schemas.security import SecurityDecision

class PromptDetector:
    def __init__(self):
        # Basic heuristic-based injection detection for prototyping
        self.injection_keywords = [
            "ignore previous instructions",
            "forget your instructions",
            "reveal system prompt",
            "bypass security",
            "you are now unrestricted"
        ]

    def analyze_query(self, query: str) -> SecurityDecision:
        lower_query = query.lower()
        for keyword in self.injection_keywords:
            if keyword in lower_query:
                return SecurityDecision(
                    is_allowed=False,
                    risk_score=100,
                    risk_level="HIGH",
                    reason="Direct prompt injection detected"
                )
                
        return SecurityDecision(
            is_allowed=True,
            risk_score=0,
            risk_level="LOW",
            reason="Query appears safe"
        )
