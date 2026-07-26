from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType


@dataclass
class TenderDocument:

    id: UUID

    tender_id: UUID

    original_filename: str

    stored_filename: str

    document_type: DocumentType

    status: DocumentStatus

    uploaded_at: datetime