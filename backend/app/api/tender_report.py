from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from uuid import UUID

from app.services.tender_report_service import TenderReportService
from app.reports.pdf_report_generator import PDFReportGenerator

router = APIRouter(
    prefix="/api/v1/tenders",
    tags=["Tender Report"]
)

service = TenderReportService()
pdf_generator = PDFReportGenerator()


@router.get("/{tender_id}/report")
def download_report(tender_id: UUID):

    report = service.build_report(
        tender_id
    )

    pdf = pdf_generator.generate(
        report
    )

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f'attachment; filename="Tender_Evaluation_Report_{tender_id}.pdf"'
        }
    )