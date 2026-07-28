from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.domain.criterion import Criterion
from app.models.criterion_model import CriterionModel


class CriterionRepository:

    def save(self, criterion: Criterion):

        with SessionLocal() as session:

            model = CriterionModel(
                id=str(criterion.id),
                tender_id=str(criterion.tender_id),
                title=criterion.title,
                description=criterion.description,
                evidence_required=criterion.evidence_required,
                mandatory=criterion.mandatory,
                created_at=criterion.created_at,
                updated_at=criterion.updated_at
            )

            session.add(model)
            session.commit()

        return criterion

    def find_by_id(self, criterion_id: UUID):

        with SessionLocal() as session:

            model = session.get(
                CriterionModel,
                str(criterion_id)
            )

            if model is None:
                return None

            return Criterion(
                id=UUID(model.id),
                tender_id=UUID(model.tender_id),
                title=model.title,
                description=model.description,
                evidence_required=model.evidence_required,
                mandatory=model.mandatory,
                created_at=model.created_at,
                updated_at=model.updated_at
            )

    def find_by_tender(self, tender_id: UUID):

        with SessionLocal() as session:

            rows = session.scalars(
                select(CriterionModel).where(
                    CriterionModel.tender_id == str(tender_id)
                )
            ).all()

            return [

                Criterion(
                    id=UUID(row.id),
                    tender_id=UUID(row.tender_id),
                    title=row.title,
                    description=row.description,
                    evidence_required=row.evidence_required,
                    mandatory=row.mandatory,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )

                for row in rows

            ]