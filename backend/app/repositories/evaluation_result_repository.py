from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.domain.evaluation_result import EvaluationResult
from app.enums.evaluation_status import EvaluationStatus
from app.models.evaluation_result_model import EvaluationResultModel


class EvaluationResultRepository:

    def save(self, result: EvaluationResult):

        with SessionLocal() as session:

            model = EvaluationResultModel(
                id=str(result.id),
                bidder_id=str(result.bidder_id),
                criterion_id=str(result.criterion_id),
                status=result.status.value,
                confidence=result.confidence,
                matched_text=result.matched_text,
                remarks=result.remarks,
                created_at=result.created_at,
                updated_at=result.updated_at
            )

            session.add(model)
            session.commit()

        return result

    def find_by_bidder(self, bidder_id: UUID):

        with SessionLocal() as session:

            rows = session.scalars(
                select(EvaluationResultModel).where(
                    EvaluationResultModel.bidder_id == str(bidder_id)
                )
            ).all()

            return [

                EvaluationResult(
                    id=UUID(row.id),
                    bidder_id=UUID(row.bidder_id),
                    criterion_id=UUID(row.criterion_id),
                    status=EvaluationStatus(row.status),
                    confidence=row.confidence,
                    matched_text=row.matched_text,
                    remarks=row.remarks,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )

                for row in rows

            ]