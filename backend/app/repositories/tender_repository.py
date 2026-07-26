from typing import Dict
from uuid import UUID

from app.domain.tender import Tender


class TenderRepository:

    _tenders = {}

    def __init__(self):
        pass
    
    def save(self, tender: Tender):
        self._tenders[tender.id] = tender
        return tender

    def find_by_id(self, tender_id: UUID):
        return self._tenders.get(tender_id)

    def find_all(self):
        return list(self._tenders.values())

    def exists_by_tender_number(self, tender_number: str):
        return any(
            tender.tender_number == tender_number
            for tender in self._tenders.values()
        )

    def delete(self, tender_id: UUID):
        if tender_id in self._tenders:
            del self._tenders[tender_id]
            return True
        return False