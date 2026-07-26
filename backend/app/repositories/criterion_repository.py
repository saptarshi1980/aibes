from typing import Dict, List
from uuid import UUID

from app.domain.criterion import Criterion


class CriterionRepository:

    _criteria: Dict[UUID, Criterion] = {}

    def save(self, criterion: Criterion):

        self._criteria[criterion.id] = criterion

        return criterion

    def find_by_id(self, criterion_id: UUID):

        return self._criteria.get(criterion_id)

    def find_by_tender(self, tender_id: UUID) -> List[Criterion]:

        return [

            criterion

            for criterion in self._criteria.values()

            if criterion.tender_id == tender_id

        ]