from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_chat, routes_documents

app = FastAPI(title="RAGShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_chat.router, prefix="/api")
app.include_router(routes_documents.router, prefix="/api")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
