from app.agents.bid_evaluation_agent import BidEvaluationAgent
from app.repositories.bidder_repository import BidderRepository
from app.repositories.criterion_repository import CriterionRepository
from app.services.document_text_service import DocumentTextService
from app.services.evaluation_result_service import EvaluationResultService
from app.enums.evaluation_status import EvaluationStatus


class EvaluationService:

    def __init__(self):

        self.criteria = CriterionRepository()

        self.bidders = BidderRepository()

        self.documents = DocumentTextService()

        self.results = EvaluationResultService()

        self.agent = BidEvaluationAgent()
        
    def evaluate_one(
    self,
    bidder_id,
    criterion_id
):

        bidder = self.bidders.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError("Bidder not found.")

        criterion = self.criteria.find_by_id(
            criterion_id
        )

        if criterion is None:
            raise ValueError("Criterion not found.")

        # Verify both belong to the same tender
        if bidder.tender_id != criterion.tender_id:
            raise ValueError(
                "Bidder and Criterion belong to different tenders."
            )

        bidder_text = self.documents.get_bidder_text(
            bidder_id
        )

        ai_result = self.agent.evaluate(
            criterion,
            bidder_text
        )

        return self.results.save_result(
            bidder_id=bidder.id,
            criterion_id=criterion.id,
            status=EvaluationStatus(
                ai_result["status"]
            ),
            confidence=ai_result["confidence"],
            matched_text=ai_result["matched_text"],
            remarks=ai_result["remarks"]
        )    