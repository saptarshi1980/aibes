from fastapi import APIRouter, UploadFile, File

from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentUploadResponse

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse
)
async def upload_document(
        file: UploadFile = File(...)
):

    result = DocumentService.save_document(file)

    return DocumentUploadResponse(
        success=True,
        message="Document uploaded successfully",
        filename=result["filename"],
        size=result["size"]
    )