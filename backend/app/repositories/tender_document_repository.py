from typing import Dict, List
from uuid import UUID

from app.domain.tender_document import TenderDocument


class TenderDocumentRepository:

    _documents: Dict[UUID, TenderDocument] = {}

    def save(self, document: TenderDocument):
        self._documents[document.id] = document
        return document

    def find_by_id(self, document_id: UUID):
        return self._documents.get(document_id)

    def find_by_tender(self, tender_id: UUID) -> List[TenderDocument]:
        return [
            doc
            for doc in self._documents.values()
            if doc.tender_id == tender_id
        ]