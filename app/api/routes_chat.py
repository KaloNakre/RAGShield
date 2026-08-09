from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/chat")
def chat(request: ChatRequest):
    return rag_service.process_chat(request.query, request.user_role)
