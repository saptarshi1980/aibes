from uuid import UUID

from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.clarification_letter_service import ClarificationLetterService


router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Clarification Letter"],
)

service = ClarificationLetterService()


class ClarificationRequest(BaseModel):
    submission_date: str


@router.post("/bidder/{bidder_id}/clarification")
def generate_clarification_letter(
    bidder_id: UUID,
    request: ClarificationRequest,
):

    content = service.generate(
        bidder_id,
        request.submission_date,
    )

    output = BytesIO()

    output.write(
        content.encode("utf-8")
    )

    output.seek(0)

    return StreamingResponse(

        output,

        media_type="text/plain",

        headers={

            "Content-Disposition":
            'attachment; filename="Clarification_Email.txt"'

        }

    )