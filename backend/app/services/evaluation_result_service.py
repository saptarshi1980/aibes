from datetime import datetime
from uuid import uuid4

from app.domain.evaluation_result import EvaluationResult
from app.repositories.evaluation_result_repository import (
    EvaluationResultRepository
)
from app.enums.evaluation_status import EvaluationStatus


class EvaluationResultService:

    def __init__(self):
        self.repository = EvaluationResultRepository()
        
    def delete_results(
    self,
    bidder_id
):

        self.repository.delete_by_bidder(
            bidder_id
        )    

    def save_result(
        self,
        bidder_id,
        criterion_id,
        status: EvaluationStatus,
        confidence,
        matched_text,
        remarks
    ):

        result = EvaluationResult(
            id=uuid4(),
            bidder_id=bidder_id,
            criterion_id=criterion_id,
            status=status,
            confidence=confidence,
            matched_text=matched_text,
            remarks=remarks,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.repository.save(result)
    
    def get_results(
    self,
    bidder_id
):

        return self.repository.find_by_bidder(
            bidder_id
        )