from collections import defaultdict

from app.repositories.evaluation_report_repository import (
    EvaluationReportRepository
)


class EvaluationReportService:

    def __init__(self):

        self.repository = EvaluationReportRepository()

    def generate_report(
        self,
        tender_id
    ):

        bidders = self.repository.get_bidders(
            tender_id
        )

        criteria = self.repository.get_criteria(
            tender_id
        )

        bidder_ids = [

            bidder.id

            for bidder in bidders

        ]

        results = self.repository.get_results(
            bidder_ids
        )

        #
        # Result Lookup
        #

        result_lookup = {}

        for result in results:

            result_lookup[

                (

                    result.bidder_id,

                    result.criterion_id

                )

            ] = result

        #
        # Bidder Summary
        #

        bidder_summary = []

        evaluated_count = 0

        for bidder in bidders:

            complied = 0
            partial = 0
            not_complied = 0
            not_found = 0
            review = 0

            has_result = False

            for criterion in criteria:

                result = result_lookup.get(

                    (

                        bidder.id,

                        criterion.id

                    )

                )

                if result is None:
                    continue

                has_result = True

                status = result.status

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

            if has_result:

                evaluated_count += 1

            bidder_summary.append({

                "id": bidder.id,

                "name": bidder.bidder_name,

                "complied": complied,

                "partial": partial,

                "not_complied": not_complied,

                "not_found": not_found,

                "needs_review": review

            })

        #
        # Matrix
        #

        matrix = []

        for criterion in criteria:

            row = {

                "criterion_id": criterion.id,

                "title": criterion.title,

                "mandatory": criterion.mandatory,

                "results": {}

            }

            for bidder in bidders:

                result = result_lookup.get(

                    (

                        bidder.id,

                        criterion.id

                    )

                )

                row["results"][

                    str(bidder.id)

                ] = (

                    result.status

                    if result

                    else "PENDING"

                )

            matrix.append(row)

        #
        # Final Report
        #

        return {

            "summary": {

                "total_bidders": len(bidders),

                "evaluated": evaluated_count,

                "pending": len(bidders) - evaluated_count,

                "total_criteria": len(criteria)

            },

            "bidders": bidder_summary,

            "matrix": matrix

        }