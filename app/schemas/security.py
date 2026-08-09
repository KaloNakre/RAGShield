from pydantic import BaseModel
from typing import Optional

class SecurityDecision(BaseModel):
    is_allowed: bool
    risk_score: int
    risk_level: str
    reason: str
