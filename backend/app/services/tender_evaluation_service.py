from app.repositories.bidder_repository import BidderRepository
from app.services.evaluation_service import EvaluationService


class TenderEvaluationService:

    def __init__(self):

        self.bidder_repository = BidderRepository()

        self.evaluation_service = EvaluationService()

    def evaluate_tender(
        self,
        tender_id
    ):

        bidders = self.bidder_repository.find_by_tender(
            tender_id
        )

        if not bidders:
            raise ValueError(
                "No bidders found for this tender."
            )

        bidder_results = []

        for bidder in bidders:

            result = self.evaluation_service.evaluate_bidder(
                bidder.id
            )

            bidder_results.append(result)

        return {
            "tender_id": tender_id,
            "total_bidders": len(bidders),
            "bidders": bidder_results
        }