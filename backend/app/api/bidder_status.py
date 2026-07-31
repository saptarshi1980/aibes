from uuid import UUID

from fastapi import APIRouter

from app.services.bidder_status_service import BidderStatusService

router = APIRouter(
    prefix="/api/v1/bidders",
    tags=["Bidder Status"]
)

service = BidderStatusService()


@router.get("/{bidder_id}/embedding-status")
def embedding_status(bidder_id: UUID):

    return service.embedding_status(
        bidder_id
    )