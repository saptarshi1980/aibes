import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        """
        Cleans extracted text from PDF/OCR.
        """

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove spaces before newlines
        text = re.sub(r" +\n", "\n", text)

        return text.strip()