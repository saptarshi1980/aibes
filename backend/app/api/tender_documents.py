from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile

from app.enums.document_type import DocumentType
from app.services.tender_document_service import TenderDocumentService

router = APIRouter(
    prefix="/api/v1/tenders",
    tags=["Tender Documents"]
)

service = TenderDocumentService()


@router.get("/{tender_id}/documents")
def get_documents(tender_id: UUID):
    return service.get_documents(tender_id)


@router.post("/{tender_id}/documents")
def upload_document(
    tender_id: UUID,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...)
):
    return service.upload_document(
        tender_id,
        document_type,
        file
    )