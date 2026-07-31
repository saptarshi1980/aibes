from uuid import UUID

from app.repositories.tender_repository import TenderRepository
from app.repositories.bidder_repository import BidderRepository
from app.repositories.criterion_repository import CriterionRepository
from app.repositories.evaluation_result_repository import (
    EvaluationResultRepository
)


class TenderReportService:

    def __init__(self):

        self.tenders = TenderRepository()

        self.bidders = BidderRepository()

        self.criteria = CriterionRepository()

        self.results = EvaluationResultRepository()

    def build_report(
        self,
        tender_id: UUID
    ):

        #
        # Tender
        #
        tender = self.tenders.find_by_id(
            tender_id
        )

        if tender is None:
            raise ValueError(
                "Tender not found."
            )

        #
        # Criteria
        #
        criteria = self.criteria.find_by_tender(
            tender_id
        )

        #
        # Bidders
        #
        bidders = self.bidders.find_by_tender(
            tender_id
        )

        bidder_summary = []

        matrix = []

        #
        # Build bidder summary
        #
        for bidder in bidders:

            results = self.results.find_by_bidder(
                bidder.id
            )

            complied = 0
            partial = 0
            not_complied = 0
            not_found = 0
            review = 0

            for result in results:

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

                    review += 1

            bidder_summary.append({

                "id": bidder.id,

                "name": bidder.bidder_name,

                "summary": {

                    "complied": complied,

                    "partial": partial,

                    "not_complied": not_complied,

                    "not_found": not_found,

                    "needs_review": review

                },

                "results": results

            })

        #
        # Build comparison matrix
        #
        for criterion in criteria:

            row = {

                "criterion_id": criterion.id,

                "title": criterion.title,

                "mandatory": criterion.mandatory,

                "bidders": []

            }

            for bidder in bidder_summary:

                result = next(

                    (
                        r
                        for r in bidder["results"]
                        if r.criterion_id == criterion.id
                    ),

                    None

                )

                if result is None:

                    row["bidders"].append({

                        "bidder_id": bidder["id"],

                        "bidder_name": bidder["name"],

                        "status": "NOT_EVALUATED",

                        "confidence": 0,

                        "remarks": "",

                        "matched_text": ""

                    })

                else:

                    row["bidders"].append({

                        "bidder_id": bidder["id"],

                        "bidder_name": bidder["name"],

                        "status": result.status.value,

                        "confidence": result.confidence,

                        "remarks": result.remarks,

                        "matched_text": result.matched_text

                    })

            matrix.append(row)

        #
        # Executive Summary
        #
        evaluated = 0

        for bidder in bidder_summary:

            if len(bidder["results"]) > 0:

                evaluated += 1

        summary = {

            "total_bidders": len(bidders),

            "evaluated": evaluated,

            "pending": len(bidders) - evaluated,

            "total_criteria": len(criteria)

        }

        #
        # Final Report Object
        #
        return {

            "tender": tender,

            "summary": summary,

            "criteria": criteria,

            "bidders": bidder_summary,

            "matrix": matrix

        }