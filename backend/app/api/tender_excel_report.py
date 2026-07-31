from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.tender_report_service import TenderReportService
from app.reports.excel_report_generator import ExcelReportGenerator

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Tender Reports"]
)

service = TenderReportService()

generator = ExcelReportGenerator()


@router.get("/tender/{tender_id}/excel")
def download_excel_report(
    tender_id: UUID
):

    report = service.build_report(
        tender_id
    )

    output = generator.generate(
        report
    )

    filename = (
        "Tender_Report_"
        +
        str(tender_id)
        +
        ".xlsx"
    )

    return StreamingResponse(

        output,

        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={

            "Content-Disposition":
            f'attachment; filename="{filename}"'

        }

    )