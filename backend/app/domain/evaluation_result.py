from dataclasses import dataclass
from uuid import UUID


@dataclass
class EvaluationResult:

    criterion_id: UUID

    bidder_id: UUID

    status: str

    confidence: float

    evidence: str

    remarks: str