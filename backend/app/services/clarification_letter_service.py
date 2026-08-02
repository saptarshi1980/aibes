from pathlib import Path
from uuid import UUID
from datetime import date
from app.repositories.criterion_repository import CriterionRepository
from app.repositories.bidder_repository import BidderRepository
from app.repositories.tender_repository import TenderRepository
from app.repositories.evaluation_result_repository import EvaluationResultRepository
from app.utils.storage_manager import StorageManager
from app.enums.evaluation_status import EvaluationStatus


class ClarificationLetterService:

    def __init__(self):

        self.bidder_repository = BidderRepository()
        self.tender_repository = TenderRepository()
        self.result_repository = EvaluationResultRepository()
        self.criterion_repository = CriterionRepository()

    def generate(
        self,
        bidder_id: UUID,
        submission_date: str
    ):

        bidder = self.bidder_repository.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError("Bidder not found.")

        tender = self.tender_repository.find_by_id(
            bidder.tender_id
        )

        if tender is None:
            raise ValueError("Tender not found.")

        results = self.result_repository.find_by_bidder(
            bidder_id
        )

        

        pending = [

            r for r in results

            if r.status in [

                EvaluationStatus.NOT_COMPLIED,
                EvaluationStatus.NOT_FOUND,
                EvaluationStatus.NEEDS_MANUAL_REVIEW

            ]

        ]

        text = []

        text.append("To")
        text.append("")
        text.append(bidder.contact_person or "")
        text.append(bidder.bidder_name)
        text.append("")
        text.append(
            f"SUB: DPL NIT No. {tender.tender_number}"
        )
        text.append("")
        text.append(
            f"Referring to your bid against our NIT No. {tender.tender_number} "
            f'for "{tender.title}", documents submitted against the following '
            f"criteria are not found to be adequate:"
        )
        text.append("")
        text.append("--------------------------------------------")

        sl = 1

        for item in pending:

            criterion = self.criterion_repository.find_by_id(
                item.criterion_id
            )

            if criterion is None:
                continue

            text.append(
                f"{sl}. {criterion.title}"
            )

            if item.remarks:

                text.append(
                    f"    Observation : {item.remarks}"
                )

            text.append("")

            sl += 1

        text.append(
            f"You are requested to kindly submit sufficient "
            f"documents as per the said NIT to this office "
            f"positively by {submission_date} to the email address corp.purchase@company_domain.com.\n\nRegards \n\nProcurement Teeam,\n\nCompany Name"
        )

        content = "\n".join(text)

        return content