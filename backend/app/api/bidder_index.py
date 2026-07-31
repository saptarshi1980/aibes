from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.services.bidder_index_service import BidderIndexService

router = APIRouter(
    prefix="/api/v1/bidders",
    tags=["Bidder Index"]
)

service = BidderIndexService()


@router.post("/{bidder_id}/generate-index")
def generate_index(bidder_id: UUID):

    try:

        return service.generate_index(
            bidder_id
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )