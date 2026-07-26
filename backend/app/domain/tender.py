from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.enums.tender_status import TenderStatus


@dataclass
class Tender:
    id: UUID
    tender_number: str
    title: str
    department: str
    issue_date: date
    closing_date: date
    status: TenderStatus
    created_at: datetime
    updated_at: datetime
    description: str | None = None