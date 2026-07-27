from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import String

from app.database.base import Base


class TenderModel(Base):

    __tablename__ = "tenders"

    id = Column(String(36), primary_key=True)

    tender_number = Column(
        String(100),
        nullable=False,
        unique=True
    )

    title = Column(
        String(500),
        nullable=False
    )

    department = Column(
        String(200),
        nullable=False
    )

    issue_date = Column(Date)

    closing_date = Column(Date)

    status = Column(
        String(30),
        nullable=False
    )

    description = Column(
        String(4000)
    )

    created_at = Column(DateTime)

    updated_at = Column(DateTime)