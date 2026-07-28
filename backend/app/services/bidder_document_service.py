from datetime import datetime
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.domain.bidder_document import BidderDocument
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.repositories.bidder_document_repository import BidderDocumentRepository
from app.repositories.bidder_repository import BidderRepository
from app.services.document_storage_service import DocumentStorageService
from app.utils.storage_manager import StorageManager


class BidderDocumentService:

    def __init__(self):

        self.repository = BidderDocumentRepository()
        self.bidder_repository = BidderRepository()

    def upload_document(
        self,
        bidder_id: UUID,
        document_type: DocumentType,
        file: UploadFile
    ):

        bidder = self.bidder_repository.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError(
                "Bidder not found."
            )

        bidder_folder = (
            StorageManager.get_bidder_documents_path(
                bidder.tender_id,
                bidder.bidder_name
            )
        )

        document_id = uuid4()

        stored_filename = (
            f"{document_type.value}_{document_id}.pdf"
        )

        DocumentStorageService.save_document(
            bidder_folder,
            stored_filename,
            file
        )

        document = BidderDocument(
            id=document_id,
            bidder_id=bidder.id,
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
        bidder_id: UUID
    ):

        return self.repository.find_by_bidder(
            bidder_id
        )