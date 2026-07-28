from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.services.evaluation_service import EvaluationService

router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Evaluation"]
)

service = EvaluationService()


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