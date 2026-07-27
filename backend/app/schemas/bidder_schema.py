from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BidderCreateRequest(BaseModel):

    tender_id: UUID

    bidder_name: str

    contact_person: str | None = None

    email: str | None = None

    phone: str |None = None


class BidderResponse(BaseModel):

    id: UUID

    tender_id: UUID

    bidder_name: str

    contact_person: str | None = None

    email: str | None = None

    phone: str | None = None

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True