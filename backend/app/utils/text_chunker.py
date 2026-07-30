class TextChunker:

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 2500,
        overlap: int = 300
    ):

        chunks = []

        start = 0

        while start < len(text):

            end = min(
                start + chunk_size,
                len(text)
            )

            chunks.append(
                text[start:end]
            )

            start = end - overlap

            if start < 0:
                start = 0

            if end == len(text):
                break

        return chunks