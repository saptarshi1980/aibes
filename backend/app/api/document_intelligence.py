from pathlib import Path
import tempfile
import os
from unittest import result


from fastapi import APIRouter, File, UploadFile

from app.document_intelligence.pdf_processor import PDFProcessor

router = APIRouter(
    prefix="/api/v1/document-intelligence",
    tags=["Document Intelligence"]
)


@router.post("/test")
async def test_pdf(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = PDFProcessor.extract_document_text(temp_path)
        

        return {
                "method": result["method"],
                "pages": result["pages"],
                "characters": len(result["text"]),
                "preview": result["text"][:1000]
                    
                }

    finally:
        os.remove(temp_path)