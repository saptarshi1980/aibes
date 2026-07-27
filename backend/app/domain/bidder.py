from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Bidder:

    id: UUID

    tender_id: UUID

    bidder_name: str

    contact_person: str | None = None

    email: str | None = None

    phone: str | None = None

    created_at: datetime | None = None

    updated_at: datetime | None = None