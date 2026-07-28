from pathlib import Path
from shutil import copyfileobj

from fastapi import UploadFile

from app.document_intelligence.pdf_processor import PDFProcessor
from app.utils.storage_manager import StorageManager


class DocumentStorageService:

    @staticmethod
    def save_document(
        destination_folder: Path,
        stored_filename: str,
        file: UploadFile
    ) -> Path:

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError(
                "Only PDF files are allowed."
            )

        destination = destination_folder / stored_filename

        with destination.open("wb") as buffer:
            copyfileobj(file.file, buffer)

        result = PDFProcessor.extract_document_text(
            str(destination)
        )

        StorageManager.save_text_file(
            destination,
            result["text"]
        )

        return destination