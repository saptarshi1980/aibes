from pdf2image import convert_from_path
import pytesseract


class OCRProcessor:

    @staticmethod
    def extract_text(pdf_path: str) -> dict:
        """
        Extract text from a scanned PDF using Tesseract OCR.
        """

        images = convert_from_path(
            pdf_path,
            poppler_path=r"C:\poppler\Library\bin"
        )

        text = ""

        for image in images:
            page_text = pytesseract.image_to_string(image, lang="eng")
            text += page_text + "\n"

        return {
            "pages": len(images),
            "text": text
        }