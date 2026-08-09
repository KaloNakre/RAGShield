from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    user_role: str = "guest"
