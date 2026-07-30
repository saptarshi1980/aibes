from datetime import datetime
from uuid import uuid4

from app.domain.tender import Tender
from app.enums.tender_status import TenderStatus
from app.repositories.tender_repository import TenderRepository
from app.utils.storage_manager import StorageManager
from fastapi import HTTPException


class TenderService:

    def __init__(self):
        self.repository = TenderRepository()

    def create_tender(self, request):

        if self.repository.exists_by_tender_number(
            request.tender_number
        ):
            raise HTTPException(
    status_code=400,
    detail="Tender number already exists."
)

        tender = Tender(
            id=uuid4(),
            tender_number=request.tender_number,
            title=request.title,
            department=request.department,
            issue_date=request.issue_date,
            closing_date=request.closing_date,
            status=TenderStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        saved_tender = self.repository.save(
            tender
        )

        StorageManager.create_tender_folder(
            saved_tender.id,
            saved_tender.tender_number
        )

        return saved_tender

    def get_all_tenders(self):

        return self.repository.find_all()

    def get_tender(
        self,
        tender_id
    ):

        return self.repository.find_by_id(
            tender_id
        )

    def update_tender(
        self,
        tender_id,
        request
    ):

        tender = self.repository.find_by_id(
            tender_id
        )

        if tender is None:
            raise ValueError(
                "Tender not found."
            )

        tender.tender_number = request.tender_number
        tender.title = request.title
        tender.department = request.department
        tender.issue_date = request.issue_date
        tender.closing_date = request.closing_date
        tender.updated_at = datetime.now()

        return self.repository.update(
            tender
        )