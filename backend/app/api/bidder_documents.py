from uuid import UUID

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.enums.document_type import DocumentType
from app.services.bidder_document_service import BidderDocumentService

router = APIRouter(
    prefix="/api/v1/bidders",
    tags=["Bidder Documents"]
)

service = BidderDocumentService()


@router.post("/{bidder_id}/documents")
def upload_document(
    bidder_id: UUID,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...)
):

    try:

        return service.upload_document(
            bidder_id,
            document_type,
            file
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )


@router.get("/{bidder_id}/documents")
def get_documents(
    bidder_id: UUID
):

    return service.get_documents(
        bidder_id
    )