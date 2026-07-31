from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.bidder_model import BidderModel
from app.models.criterion_model import CriterionModel
from app.models.evaluation_result_model import EvaluationResultModel


class EvaluationReportRepository:

    def get_bidders(
        self,
        tender_id: UUID
    ):

        with SessionLocal() as session:

            return session.scalars(

                select(BidderModel).where(

                    BidderModel.tender_id == str(tender_id)

                )

            ).all()


    def get_criteria(
        self,
        tender_id: UUID
    ):

        with SessionLocal() as session:

            return session.scalars(

                select(CriterionModel).where(

                    CriterionModel.tender_id == str(tender_id)

                )

            ).all()


    def get_results(
        self,
        bidder_ids
    ):

        with SessionLocal() as session:

            return session.scalars(

                select(EvaluationResultModel).where(

                    EvaluationResultModel.bidder_id.in_(

                        [str(x) for x in bidder_ids]

                    )

                )

            ).all()