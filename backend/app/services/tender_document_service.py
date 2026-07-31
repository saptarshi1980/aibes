from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException
from fastapi import UploadFile

from app.domain.tender_document import TenderDocument
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.repositories.criterion_repository import CriterionRepository
from app.repositories.tender_document_repository import (
    TenderDocumentRepository,
)
from app.services.document_storage_service import (
    DocumentStorageService,
)
from app.utils.storage_manager import StorageManager


class TenderDocumentService:

    def __init__(self):

        self.repository = TenderDocumentRepository()

        self.criteria_repository = CriterionRepository()

    def upload_document(
        self,
        tender_id: UUID,
        document_type: DocumentType,
        file: UploadFile
    ):

        #
        # Existing upload logic unchanged
        #

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError(
                "Only PDF files are allowed."
            )

        #
        # Allow only one NIT
        #

        if document_type == DocumentType.NIT:

            existing = self.repository.find_nit_by_tender(
                tender_id
            )

            if existing:

                raise HTTPException(
                    status_code=400,
                    detail="An NIT already exists for this Tender. Delete the existing NIT before uploading a new one."
                )

        document_folder = StorageManager.get_tender_documents_path(
            tender_id
        )

        document_id = uuid4()

        stored_filename = (
            f"{document_type.value}_{document_id}.pdf"
        )

        DocumentStorageService.save_document(
            document_folder,
            stored_filename,
            file
        )

        document = TenderDocument(

            id=document_id,

            tender_id=tender_id,

            original_filename=file.filename,

            stored_filename=stored_filename,

            document_type=document_type,

            status=DocumentStatus.UPLOADED,

            uploaded_at=datetime.now()

        )

        return self.repository.save(
            document
        )

    def get_documents(
        self,
        tender_id: UUID
    ):

        return self.repository.find_by_tender(
            tender_id
        )

    # -----------------------------------------------------
    # DELETE DOCUMENT
    # -----------------------------------------------------

    def delete_document(
        self,
        document_id: UUID
    ):

        document = self.repository.find_by_id(
            document_id
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        #
        # Business Rule
        #

        if document.document_type != DocumentType.NIT:

            raise HTTPException(
                status_code=400,
                detail="Only NIT can be deleted."
            )

        #
        # Locate folder
        #

        document_folder = StorageManager.get_tender_documents_path(
            document.tender_id
        )

        pdf_file = (
            document_folder /
            document.stored_filename
        )

        txt_file = pdf_file.with_suffix(".txt")

        #
        # Delete PDF
        #

        if pdf_file.exists():
            pdf_file.unlink()

        #
        # Delete OCR text
        #

        if txt_file.exists():
            txt_file.unlink()
            
        #
# Delete Eligibility Preview
#

        preview_file = document_folder / "eligibility_preview.txt"

        if preview_file.exists():

            preview_file.unlink()
        
        
        for chunk_file in document_folder.glob("chunk_*.txt"):    
            if chunk_file.exists():
            
                chunk_file.unlink()

        

        
        #
        # TODO (Future)
        #
        # Delete Vector Store files
        #

        #
        # Delete Criteria
        #

        self.criteria_repository.delete_by_tender(
            document.tender_id
        )

        #
        # Delete Database Record
        #

        self.repository.delete(
            document.id
        )

        return {
            "message": "NIT deleted successfully."
        }