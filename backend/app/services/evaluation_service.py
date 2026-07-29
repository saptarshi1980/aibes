import logging

from app.agents.bid_evaluation_agent import BidEvaluationAgent
from app.enums.evaluation_status import EvaluationStatus
from app.repositories.bidder_repository import BidderRepository
from app.repositories.criterion_repository import CriterionRepository
#from app.services.document_retriever import DocumentRetriever
from app.rag.rag_retriever import RAGRetriever
from app.services.evaluation_result_service import EvaluationResultService

logger = logging.getLogger(__name__)


class EvaluationService:

    def __init__(self):

        self.criteria = CriterionRepository()

        self.bidders = BidderRepository()

        self.results = EvaluationResultService()

        self.agent = BidEvaluationAgent()

        #self.retriever = DocumentRetriever()
        self.retriever = RAGRetriever()

    def normalize_status(
        self,
        status: str
    ) -> EvaluationStatus:

        status = status.strip().upper()

        mapping = {

            "N/A": "COMPLIED",

            "NA": "COMPLIED",

            "NOT APPLICABLE": "COMPLIED",

            "APPLICABLE": "COMPLIED"

        }

        status = mapping.get(
            status,
            status
        )

        return EvaluationStatus(status)

    def evaluate_one(
        self,
        bidder_id,
        criterion_id
    ):

        logger.info(
            "Evaluating Criterion %s",
            criterion_id
        )

        bidder = self.bidders.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError(
                "Bidder not found."
            )

        criterion = self.criteria.find_by_id(
            criterion_id
        )

        if criterion is None:
            raise ValueError(
                "Criterion not found."
            )

        if bidder.tender_id != criterion.tender_id:
            raise ValueError(
                "Bidder and Criterion belong to different tenders."
            )

        bidder_text = self.retriever.retrieve(
            bidder_id,
            criterion
        )

        logger.info(
            "Retriever returned %d characters",
            len(bidder_text)
        )

        ai_result = self.agent.evaluate(
            criterion,
            bidder_text
        )

        logger.info(
            "AI Result : %s",
            ai_result
        )

        status = self.normalize_status(
            ai_result["status"]
        )

        return self.results.save_result(
            bidder_id=bidder.id,
            criterion_id=criterion.id,
            status=status,
            confidence=ai_result["confidence"],
            matched_text=ai_result["matched_text"],
            remarks=ai_result["remarks"]
        )

    def evaluate_bidder(
        self,
        bidder_id
    ):

        bidder = self.bidders.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError(
                "Bidder not found."
            )

        criteria = self.criteria.find_by_tender(
            bidder.tender_id
        )

        if not criteria:
            raise ValueError(
                "No criteria found for this tender."
            )

        evaluation_details = []

        complied = 0
        partial = 0
        not_complied = 0
        not_found = 0
        needs_review = 0

        for criterion in criteria:

            result = self.evaluate_one(
                bidder.id,
                criterion.id
            )

            status = result.status.value

            if status == "COMPLIED":
                complied += 1

            elif status == "PARTIALLY_COMPLIED":
                partial += 1

            elif status == "NOT_COMPLIED":
                not_complied += 1

            elif status == "NOT_FOUND":
                not_found += 1

            else:
                needs_review += 1

            evaluation_details.append({

                "criterion_id": criterion.id,

                "title": criterion.title,

                "mandatory": criterion.mandatory,

                "status": status,

                "confidence": result.confidence,

                "remarks": result.remarks,

                "matched_text": result.matched_text

            })

        return {

            "bidder_id": bidder.id,

            "bidder_name": bidder.bidder_name,

            "summary": {

                "total_criteria": len(criteria),

                "complied": complied,

                "partially_complied": partial,

                "not_complied": not_complied,

                "not_found": not_found,

                "needs_manual_review": needs_review

            },

            "criteria": evaluation_details

        }
        
    def get_results(
    self,
    bidder_id
):

        results = self.results.get_results(
            bidder_id
        )

        output = []

        for result in results:

            criterion = self.criteria.find_by_id(
                result.criterion_id
            )

            output.append({

                "id": result.id,

                "criterion_id": result.criterion_id,

                "criterion_title": criterion.title,

                "mandatory": criterion.mandatory,

                "status": result.status.value,

                "confidence": result.confidence,

                "remarks": result.remarks,

                "matched_text": result.matched_text

            })

        return output    