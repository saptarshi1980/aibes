from uuid import UUID

from fastapi import APIRouter

from app.schemas.criterion_schema import (
    CriterionCreateRequest,
    CriterionResponse
)

from app.services.criterion_service import CriterionService
from app.services.criterion_extraction_service import CriterionExtractionService

router = APIRouter(
    prefix="/api/v1/criteria",
    tags=["Criteria"]
)

service = CriterionService()
extraction_service = CriterionExtractionService()


@router.post(
    "",
    response_model=CriterionResponse
)
def create_criterion(request: CriterionCreateRequest):

    return service.create_criterion(request)


@router.get("/{tender_id}")
def get_criteria(tender_id: UUID):

    return service.get_by_tender(tender_id)


@router.post("/extract/{tender_id}")
def extract_criteria(tender_id: UUID):

    criteria = extraction_service.extract_from_tender(
        tender_id
    )

    return {
        "message": "Criteria extracted successfully.",
        "count": len(criteria)
    }
    
@router.post("/rebuild/{tender_id}")
def rebuild_criteria(tender_id: UUID):

    criteria = extraction_service.extract_from_tender(
        tender_id
    )

    return {
        "message": "Criteria rebuilt successfully.",
        "count": len(criteria)
    }    