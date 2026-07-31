from uuid import UUID

from app.database import SessionLocal
from app.domain.evaluation_result import EvaluationResult


class EvaluationResultRepository:

    def exists_by_bidder(
        self,
        bidder_id: UUID
    ):

        session = SessionLocal()

        try:

            return (

                session.query(EvaluationResult)

                .filter(
                    EvaluationResult.bidder_id == bidder_id
                )

                .first()

                is not None

            )

        finally:

            session.close()