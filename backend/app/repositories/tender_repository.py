from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.domain.tender import Tender
from app.enums.tender_status import TenderStatus
from app.models.tender_model import TenderModel


class TenderRepository:

    def save(self, tender: Tender):

        with SessionLocal() as session:

            model = TenderModel(
                id=str(tender.id),
                tender_number=tender.tender_number,
                title=tender.title,
                department=tender.department,
                issue_date=tender.issue_date,
                closing_date=tender.closing_date,
                status=tender.status.value,
                description=tender.description,
                created_at=tender.created_at,
                updated_at=tender.updated_at
            )

            session.add(model)
            session.commit()

        return tender

    def find_by_id(self, tender_id: UUID):

        with SessionLocal() as session:

            model = session.get(
                TenderModel,
                str(tender_id)
            )

            if model is None:
                return None

            return Tender(
                id=UUID(model.id),
                tender_number=model.tender_number,
                title=model.title,
                department=model.department,
                issue_date=model.issue_date,
                closing_date=model.closing_date,
                status=TenderStatus(model.status),
                description=model.description,
                created_at=model.created_at,
                updated_at=model.updated_at
            )

    def find_all(self):

        with SessionLocal() as session:

            rows = session.scalars(
                select(TenderModel)
            ).all()

            return [
                Tender(
                    id=UUID(row.id),
                    tender_number=row.tender_number,
                    title=row.title,
                    department=row.department,
                    issue_date=row.issue_date,
                    closing_date=row.closing_date,
                    status=TenderStatus(row.status),
                    description=row.description,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
                for row in rows
            ]

    def exists_by_tender_number(self, tender_number: str):

        with SessionLocal() as session:

            stmt = select(TenderModel).where(
                TenderModel.tender_number == tender_number
            )

            return session.scalar(stmt) is not None

    def delete(self, tender_id: UUID):

        with SessionLocal() as session:

            model = session.get(
                TenderModel,
                str(tender_id)
            )

            if model is None:
                return False

            session.delete(model)
            session.commit()

            return True
    
    def update(self, tender: Tender):

        with SessionLocal() as session:

            model = session.get(
            TenderModel,
            str(tender.id)
            )

            if model is None:
                return None

            model.tender_number = tender.tender_number
            model.title = tender.title
            model.department = tender.department
            model.issue_date = tender.issue_date
            model.closing_date = tender.closing_date
            model.description = tender.description
            model.status = tender.status.value
            model.updated_at = tender.updated_at

            session.commit()

            return Tender(
                    id=UUID(model.id),
                    tender_number=model.tender_number,
                    title=model.title,
                    department=model.department,
                    issue_date=model.issue_date,
                    closing_date=model.closing_date,
                    status=TenderStatus(model.status),
                    description=model.description,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )    