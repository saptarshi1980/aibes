from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.domain.bidder import Bidder
from app.models.bidder_model import BidderModel


class BidderRepository:

    def save(self, bidder: Bidder):

        with SessionLocal() as session:

            model = BidderModel(
                id=str(bidder.id),
                tender_id=str(bidder.tender_id),
                bidder_name=bidder.bidder_name,
                contact_person=bidder.contact_person,
                email=bidder.email,
                phone=bidder.phone,
                created_at=bidder.created_at,
                updated_at=bidder.updated_at
            )

            session.add(model)
            session.commit()

        return bidder

    def find_by_id(self, bidder_id: UUID):

        with SessionLocal() as session:

            model = session.get(
                BidderModel,
                str(bidder_id)
            )

            if model is None:
                return None

            return Bidder(
                id=UUID(model.id),
                tender_id=UUID(model.tender_id),
                bidder_name=model.bidder_name,
                contact_person=model.contact_person,
                email=model.email,
                phone=model.phone,
                created_at=model.created_at,
                updated_at=model.updated_at
            )

    def find_by_tender(self, tender_id: UUID):

        with SessionLocal() as session:

            rows = session.scalars(
                select(BidderModel).where(
                    BidderModel.tender_id == str(tender_id)
                )
            ).all()

            return [

                Bidder(
                    id=UUID(row.id),
                    tender_id=UUID(row.tender_id),
                    bidder_name=row.bidder_name,
                    contact_person=row.contact_person,
                    email=row.email,
                    phone=row.phone,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )

                for row in rows

            ]