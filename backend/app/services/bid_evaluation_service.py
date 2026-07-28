from app.agents.bid_evaluation_agent import BidEvaluationAgent

from app.repositories.bidder_repository import BidderRepository
from app.repositories.criterion_repository import CriterionRepository
from app.repositories.bidder_document_repository import BidderDocumentRepository


class BidEvaluationService:

    def __init__(self):

        self.agent = BidEvaluationAgent()

        self.bidder_repository = BidderRepository()
        self.criterion_repository = CriterionRepository()
        self.bidder_document_repository = BidderDocumentRepository()

    def evaluate_bidder(
        self,
        bidder_id
    ):

        bidder = self.bidder_repository.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError("Bidder not found.")

        criteria = self.criterion_repository.find_by_tender(
            bidder.tender_id
        )

        documents = self.bidder_document_repository.find_by_bidder(
            bidder.id
        )

        print(criteria)
        print(documents)