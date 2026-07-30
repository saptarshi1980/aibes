from datetime import datetime
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.domain.tender_document import TenderDocument
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.repositories.tender_document_repository import TenderDocumentRepository
from app.services.document_storage_service import DocumentStorageService
from app.utils.storage_manager import StorageManager


class TenderDocumentService:

    def __init__(self):

        self.repository = TenderDocumentRepository()

    def upload_document(
        self,
        tender_id: UUID,
        document_type: DocumentType,
        file: UploadFile
    ):

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are allowed.")

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

        return self.repository.save(document)

    def get_documents(self, tender_id: UUID):

        return self.repository.find_by_tender(
            tender_id
        )