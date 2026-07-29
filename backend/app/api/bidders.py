from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.bidder_schema import (
    BidderCreateRequest,
    BidderResponse
)

from app.services.bidder_service import BidderService

router = APIRouter(
    prefix="/api/v1/bidders",
    tags=["Bidders"]
)

service = BidderService()


@router.post(
    "",
    response_model=BidderResponse
)
def create_bidder(request: BidderCreateRequest):

    try:

        return service.create_bidder(request)

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )


@router.get(
    "/tender/{tender_id}",
    response_model=list[BidderResponse]
)
def get_bidders(tender_id: UUID):

    return service.get_bidders(tender_id)

@router.get(
    "/{bidder_id}",
    response_model=BidderResponse
)
def get_bidder(bidder_id: UUID):

    bidder = service.get_bidder(
        bidder_id
    )

    if bidder is None:

        raise HTTPException(
            status_code=404,
            detail="Bidder not found."
        )

    return bidder