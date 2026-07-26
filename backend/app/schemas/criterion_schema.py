from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CriterionCreateRequest(BaseModel):

    tender_id: UUID

    criterion_number: str

    title: str

    description: str

    evidence_required: str

    mandatory: bool


class CriterionResponse(BaseModel):

    id: UUID

    tender_id: UUID

    criterion_number: str

    title: str

    description: str

    evidence_required: str

    mandatory: bool

    created_at: datetime

    updated_at: datetime