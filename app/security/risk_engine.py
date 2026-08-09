from app.schemas.security import SecurityDecision

class RiskEngine:
    def calculate_overall_risk(self, prompt_decision: SecurityDecision, doc_risk: int) -> SecurityDecision:
        total_score = prompt_decision.risk_score + doc_risk
        
        # Cap at 100
        total_score = min(total_score, 100)
        
        if total_score <= 20:
            level = "LOW"
            allowed = True
        elif total_score <= 50:
            level = "MEDIUM"
            allowed = True
        else:
            level = "HIGH"
            allowed = False
            
        return SecurityDecision(
            is_allowed=allowed,
            risk_score=total_score,
            risk_level=level,
            reason="Calculated from aggregate risks"
        )
