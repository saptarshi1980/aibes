from pathlib import Path
import shutil

from app.document_intelligence.pdf_processor import PDFProcessor
from app.utils.storage_manager import StorageManager
from app.utils.storage_manager import StorageManager


UPLOAD_FOLDER = Path("uploads")


class DocumentService:

    @staticmethod
    def save_document(file):

        UPLOAD_FOLDER.mkdir(exist_ok=True)

        file_path = UPLOAD_FOLDER / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": file.filename,
            "path": file_path,
            "size": file_path.stat().st_size
        }

    @staticmethod
    def process_document(pdf_path: Path):

        result = DocumentIntelligence.extract_text(
            pdf_path
        )

        StorageManager.save_text_file(
            pdf_path,
            result["text"]
        )

        return result
    
    @staticmethod
    def process_pdf(pdf_path: Path):

        result = PDFProcessor.extract_document_text(
        str(pdf_path)
    )

        StorageManager.save_text_file(
        pdf_path,
        result["text"]
    )

        return result