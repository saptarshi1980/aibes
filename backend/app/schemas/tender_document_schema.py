from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType


class TenderDocumentResponse(BaseModel):

    id: UUID

    tender_id: UUID

    original_filename: str

    stored_filename: str

    document_type: DocumentType

    status: DocumentStatus

    uploaded_at: datetime