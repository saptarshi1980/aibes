from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.tender_schema import (
    TenderCreateRequest,
    TenderResponse,
)
from app.services.tender_service import TenderService

router = APIRouter(
    prefix="/api/v1/tenders",
    tags=["Tenders"]
)

service = TenderService()


@router.post("", response_model=TenderResponse)
def create_tender(request: TenderCreateRequest):
    try:
        return service.create_tender(request)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("", response_model=list[TenderResponse])
def get_all_tenders():
    return service.get_all_tenders()


@router.get("/{tender_id}", response_model=TenderResponse)
def get_tender(tender_id: UUID):

    tender = service.get_tender(tender_id)

    if tender is None:
        raise HTTPException(
            status_code=404,
            detail="Tender not found."
        )

    return tender