from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String

from app.database.base import Base


class BidderModel(Base):

    __tablename__ = "bidders"

    id = Column(
        String(36),
        primary_key=True
    )

    tender_id = Column(
        String(36),
        ForeignKey("tenders.id"),
        nullable=False
    )

    bidder_name = Column(
        String(300),
        nullable=False
    )

    contact_person = Column(
        String(200)
    )

    email = Column(
        String(200)
    )

    phone = Column(
        String(50)
    )

    created_at = Column(DateTime)

    updated_at = Column(DateTime)