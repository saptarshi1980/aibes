from unittest import result

import fitz
from app.ocr.ocr_processor import OCRProcessor
from app.document_intelligence.text_cleaner import TextCleaner

class PDFProcessor:

    @staticmethod
    def is_searchable(pdf_path: str) -> bool:
        """
        Returns True if at least one page contains searchable text.
        """
        doc = fitz.open(pdf_path)

        try:
            for page in doc:
                text = page.get_text().strip()
                if text:
                    return True
            return False
        finally:
            doc.close()
            
            
    @staticmethod
    def extract_text(pdf_path: str):
        doc = fitz.open(pdf_path)

        try:
            text = ""

            for page in doc:
                text += page.get_text()

            return {
                "pages": doc.page_count,
                "text": text
            }

        finally:
            doc.close()
            
    @staticmethod
    def extract_document_text(pdf_path: str):
        """
        Returns extracted text irrespective of PDF type.
        """

        if PDFProcessor.is_searchable(pdf_path):
            result = PDFProcessor.extract_text(pdf_path)
            result["text"] = TextCleaner.clean(result["text"])
            result["method"] = "DIRECT_TEXT"
            return result

        result = OCRProcessor.extract_text(pdf_path)
        result["text"] = TextCleaner.clean(result["text"])
        result["method"] = "OCR"
        return result
        