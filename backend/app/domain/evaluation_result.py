from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.enums.evaluation_status import EvaluationStatus

@dataclass
class EvaluationResult:

    id: UUID

    bidder_id: UUID

    criterion_id: UUID

    status: EvaluationStatus

    confidence: float

    matched_text: str

    remarks: str

    created_at: datetime

    updated_at: datetime