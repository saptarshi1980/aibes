from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel

from app.enums.tender_status import TenderStatus


class TenderCreateRequest(BaseModel):
    tender_number: str
    title: str
    department: str
    issue_date: date
    closing_date: date


class TenderResponse(BaseModel):
    id: UUID
    tender_number: str
    title: str
    department: str
    issue_date: date
    closing_date: date
    status: TenderStatus
    created_at: datetime