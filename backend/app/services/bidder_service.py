from datetime import datetime
from uuid import uuid4, UUID

from app.domain.bidder import Bidder
from app.repositories.bidder_repository import BidderRepository


class BidderService:

    def __init__(self):
        self.repository = BidderRepository()

    def create_bidder(self, request):

        bidder = Bidder(
            id=uuid4(),
            tender_id=request.tender_id,
            bidder_name=request.bidder_name,
            contact_person=request.contact_person,
            email=request.email,
            phone=request.phone,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.repository.save(bidder)

    def get_bidders(self, tender_id: UUID):

        return self.repository.find_by_tender(
            tender_id
        )
    def get_bidder(self, bidder_id: UUID):

        return self.repository.find_by_id(
            bidder_id
        )