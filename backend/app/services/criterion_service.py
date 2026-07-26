from datetime import datetime
from uuid import uuid4, UUID

from app.domain.criterion import Criterion
from app.repositories.criterion_repository import CriterionRepository


class CriterionService:

    def __init__(self):
        self.repository = CriterionRepository()

    def create_criterion(self, request):

        criterion = Criterion(
            id=uuid4(),
            tender_id=request.tender_id,
            criterion_number=request.criterion_number,
            title=request.title,
            description=request.description,
            evidence_required=request.evidence_required,
            mandatory=request.mandatory,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.repository.save(criterion)

    def get_criteria(self, tender_id: UUID):
        return self.repository.find_by_tender(tender_id)