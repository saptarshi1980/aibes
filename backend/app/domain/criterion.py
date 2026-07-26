from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Criterion:

    id: UUID

    tender_id: UUID

    criterion_number: str

    title: str

    description: str

    evidence_required: str

    mandatory: bool

    created_at: datetime

    updated_at: datetime