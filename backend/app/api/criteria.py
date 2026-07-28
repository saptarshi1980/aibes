from uuid import UUID

from fastapi import APIRouter

from app.schemas.criterion_schema import (
    CriterionCreateRequest,
    CriterionResponse
)
from app.services.criterion_service import CriterionService

router = APIRouter(
    prefix="/api/v1/criteria",
    tags=["Criteria"]
)

service = CriterionService()


@router.post(
    "",
    response_model=CriterionResponse
)
def create_criterion(request: CriterionCreateRequest):

    return service.create_criterion(request)


@router.get(
    "/{tender_id}"
)
def get_criteria(tender_id: UUID):

    return service.get_by_tender(tender_id)