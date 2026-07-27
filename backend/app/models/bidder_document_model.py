from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String

from app.database.base import Base


class BidderDocumentModel(Base):

    __tablename__ = "bidder_documents"

    id = Column(
        String(36),
        primary_key=True
    )

    bidder_id = Column(
        String(36),
        ForeignKey("bidders.id"),
        nullable=False
    )

    original_filename = Column(
        String(300),
        nullable=False
    )

    stored_filename = Column(
        String(300),
        nullable=False
    )

    document_type = Column(
        String(50),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False
    )

    uploaded_at = Column(
        DateTime
    )