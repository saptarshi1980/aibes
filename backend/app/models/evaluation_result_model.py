from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from app.database.base import Base


class EvaluationResultModel(Base):

    __tablename__ = "evaluation_results"

    id = Column(
        String(36),
        primary_key=True
    )

    bidder_id = Column(
        String(36),
        ForeignKey("bidders.id"),
        nullable=False
    )

    criterion_id = Column(
        String(36),
        ForeignKey("criteria.id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    matched_text = Column(
        Text
    )

    remarks = Column(
        Text
    )

    created_at = Column(
        DateTime
    )

    updated_at = Column(
        DateTime
    )