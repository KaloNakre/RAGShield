# RAGShield

Secure Retrieval-Augmented Generation System

A secure Retrieval-Augmented Generation (RAG) system with token optimization, document access controls, and prompt injection defense.

## Overview
RAGShield is a secure RAG prototype with token optimization, document access controls, and prompt injection defense.

## Problem Statement
RAG systems typically blindly trust both the user's prompt and the retrieved context. This opens up vulnerabilities like Prompt Injection (Direct and Indirect), Data Leakage, and excessive token consumption.

## RAG Architecture
- Document ingestion via PDF/TXT
- Text Chunking and Embeddings
- Vector Database using ChromaDB
- Semantic Retrieval

## Security Architecture
- Query Input Validation (Direct Prompt Injection Detection)
- Document Scanning (Indirect Prompt Injection Detection)
- Access Control (Guest, Employee, Admin roles)
- Risk Engine for overall decision making
- Output Security filter to prevent data leakage

## Features
- Complete FastAPI backend
- Modular security components
- Vanilla HTML/CSS/JS frontend dashboard
- Context Optimizer for Token reduction

## Technology Stack
- Python, FastAPI, Pydantic
- ChromaDB, sentence-transformers
- Pytest for automated testing

## Installation & Running the Application
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000` to view the UI.

## Threat Model
See `docs/threat_model.md` for a comprehensive overview of the threats and controls.

## License
MIT
