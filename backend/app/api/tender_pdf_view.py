from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.repositories.tender_document_repository import TenderDocumentRepository
from app.repositories.tender_repository import TenderRepository
from app.utils.storage_manager import StorageManager

router = APIRouter(
    prefix="/api/v1",
    tags=["Tender Documents"]
)

document_repository = TenderDocumentRepository()
tender_repository = TenderRepository()


@router.get("/documents/{document_id}/view")
def view_tender_document(document_id: UUID):

    document = document_repository.find_by_id(document_id)
    
    print(document)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    tender = tender_repository.find_by_id(
        document.tender_id
    )
    
    print(tender)

    if tender is None:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    documents_folder = StorageManager.get_tender_documents_path(
        tender.id
    )

    pdf_path = documents_folder / document.stored_filename
    
    print("PDF Path:", pdf_path)
    print("Exists:", pdf_path.exists())

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=document.original_filename
    )