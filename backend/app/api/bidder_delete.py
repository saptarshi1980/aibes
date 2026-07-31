from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException

from app.services.bidder_delete_service import BidderDeleteService

router = APIRouter(
    prefix="/api/v1/bidders",
    tags=["Bidder Delete"]
)

service = BidderDeleteService()


@router.delete("/{bidder_id}")
def delete_bidder(
    bidder_id: UUID
):

    try:

        return service.delete_bidder(
            bidder_id
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )