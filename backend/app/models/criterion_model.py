from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String

from app.database.base import Base


class CriterionModel(Base):

    __tablename__ = "criteria"

    id = Column(
        String(36),
        primary_key=True
    )

    tender_id = Column(
        String(36),
        ForeignKey("tenders.id"),
        nullable=False
    )

    

    title = Column(
        String(500),
        nullable=False
    )

    description = Column(
        String(4000)
    )

    evidence_required = Column(
        String(4000)
    )

    mandatory = Column(
        Boolean,
        nullable=False
    )

    created_at = Column(
        DateTime
    )

    updated_at = Column(
        DateTime
    )