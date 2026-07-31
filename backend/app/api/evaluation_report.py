from uuid import UUID

from fastapi import APIRouter

from app.services.evaluation_report_service import (
    EvaluationReportService
)

router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Tender Evaluation Report"]
)

service = EvaluationReportService()


@router.get("/tender/{tender_id}/report")
def tender_report(
    tender_id: UUID
):

    return service.generate_report(
        tender_id
    )