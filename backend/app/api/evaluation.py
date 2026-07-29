from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.services.evaluation_service import EvaluationService
from app.services.tender_evaluation_service import TenderEvaluationService

router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Evaluation"]
)

service = EvaluationService()
tender_service = TenderEvaluationService()


@router.post("/criterion/{bidder_id}/{criterion_id}")
def evaluate(
    bidder_id: UUID,
    criterion_id: UUID
):
    try:
        return service.evaluate_one(
            bidder_id,
            criterion_id
        )

    except ValueError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )        
@router.post("/bidder/{bidder_id}")
def evaluate_bidder(
    bidder_id: UUID
):
    try:

        return service.evaluate_bidder(
            bidder_id
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
        
@router.post("/tender/{tender_id}")
def evaluate_tender(
    tender_id: UUID
):
    try:

        return tender_service.evaluate_tender(
            tender_id
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )        