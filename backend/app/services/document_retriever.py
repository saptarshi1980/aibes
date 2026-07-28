import re

from app.repositories.bidder_document_repository import (
    BidderDocumentRepository,
)
from app.services.document_text_service import (
    DocumentTextService,
)


class DocumentRetriever:

    MAX_RETURN_CHARS = 5000
    MIN_SCORE = 2

    def __init__(self):

        self.documents = BidderDocumentRepository()
        self.text_service = DocumentTextService()

    def retrieve(
        self,
        bidder_id,
        criterion
    ) -> str:

        text = self.text_service.get_bidder_text(
            bidder_id
        )

        if not text:
            return ""

        keywords = self._extract_keywords(
            criterion
        )

        paragraphs = self._split_into_paragraphs(
            text
        )

        scored = []

        for paragraph in paragraphs:

            score = self._score_paragraph(
                paragraph,
                keywords
            )

            if score >= self.MIN_SCORE:
                scored.append(
                    (
                        score,
                        paragraph
                    )
                )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        result = []
        total_chars = 0

        for score, paragraph in scored:

            if total_chars >= self.MAX_RETURN_CHARS:
                break

            result.append(paragraph)

            total_chars += len(paragraph)

        print("=" * 80)
        print("Retriever Statistics")
        print("=" * 80)
        print("Keywords :", keywords)
        print("Paragraphs analysed :", len(paragraphs))
        print("Relevant paragraphs :", len(result))
        print("Characters returned :", total_chars)
        print("=" * 80)

        return "\n\n".join(result)

    def _split_into_paragraphs(
        self,
        text
    ):

        paragraphs = re.split(
            r"\n\s*\n",
            text
        )

        cleaned = []

        for p in paragraphs:

            p = p.strip()

            if len(p) > 40:
                cleaned.append(p)

        return cleaned

    def _score_paragraph(
        self,
        paragraph,
        keywords
    ):

        score = 0

        paragraph_lower = paragraph.lower()

        for keyword in keywords:

            keyword = keyword.lower()

            if keyword in paragraph_lower:

                if len(keyword) >= 10:
                    score += 4

                elif len(keyword) >= 7:
                    score += 3

                elif len(keyword) >= 5:
                    score += 2

                else:
                    score += 1

        return score

    def _extract_keywords(
        self,
        criterion
    ):

        text = " ".join(
            [
                criterion.title,
                criterion.description,
                criterion.evidence_required,
            ]
        ).lower()

        words = re.findall(
            r"[a-zA-Z]{4,}",
            text
        )

        stop_words = {

            "shall",
            "should",
            "their",
            "there",
            "which",
            "where",
            "whose",
            "copy",
            "document",
            "documents",
            "required",
            "mandatory",
            "provide",
            "provided",
            "proof",
            "evidence",
            "submit",
            "submitted",
            "bidder",
            "bidders",
            "must",
            "have",
            "been",
            "than",
            "this",
            "that",
            "with",
            "from",
            "under",
            "valid",
        }

        keywords = []

        for word in words:

            if word not in stop_words:

                keywords.append(word)

        return list(set(keywords))