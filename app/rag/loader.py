import os
from pypdf import PdfReader

class DocumentLoader:
    def __init__(self):
        pass

    def load_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def load_document(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            return self.load_txt(file_path)
        elif ext == '.pdf':
            return self.load_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
