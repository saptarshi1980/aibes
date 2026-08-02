from uuid import UUID

from fastapi import APIRouter

from pydantic import BaseModel

from app.services.clarification_letter_service import (
    ClarificationLetterService
)

router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Clarification Letter"]
)

service = ClarificationLetterService()


class ClarificationRequest(BaseModel):

    submission_date: str


@router.post("/bidder/{bidder_id}/clarification")
def generate_clarification_letter(
    bidder_id: UUID,
    request: ClarificationRequest
):

    return service.generate(
        bidder_id,
        request.submission_date
    )