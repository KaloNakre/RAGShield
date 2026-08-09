from fastapi import APIRouter, UploadFile, File, Form
from app.services.rag_service import RAGService
import shutil
import os

router = APIRouter()
rag_service = RAGService()

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    access_level: str = Form(...)
):
    upload_dir = "./data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    result = rag_service.upload_document(file_path, classification=access_level, access_level=access_level)
    return result
