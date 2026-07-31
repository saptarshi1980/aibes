from datetime import datetime
from uuid import UUID, uuid4
import os

from fastapi import UploadFile

from app.domain.bidder_document import BidderDocument
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.repositories.bidder_document_repository import BidderDocumentRepository
from app.repositories.bidder_repository import BidderRepository
from app.rag.vector_store import VectorStore
from app.services.document_service import DocumentService
from app.services.document_storage_service import DocumentStorageService
from app.utils.storage_manager import StorageManager


class BidderDocumentService:

    def __init__(self):

        self.repository = BidderDocumentRepository()

        self.bidder_repository = BidderRepository()

        self.vector_store = VectorStore()

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

        bidder_folder = StorageManager.get_bidder_documents_path(
            bidder.tender_id,
            bidder.bidder_name
        )

        #
        # Replace existing Technical Bid
        #

        if document_type == DocumentType.TECHNICAL_BID:

            existing = self.repository.find_technical_bid(
                bidder_id
            )

            if existing:

                #
                # Delete old PDF
                #

                pdf_path = os.path.join(
                    bidder_folder,
                    existing.stored_filename
                )

                if os.path.exists(pdf_path):

                    os.remove(pdf_path)

                #
                # Delete old TXT
                #

                txt_path = pdf_path.replace(
                    ".pdf",
                    ".txt"
                )

                if os.path.exists(txt_path):

                    os.remove(txt_path)

                #
                # Delete Vector DB
                #

                self.vector_store.delete(
                    bidder_id
                )

                #
                # Delete old database record
                #

                self.repository.delete(
                    existing.id
                )

        #
        # Save new PDF
        #

        document_id = uuid4()

        stored_filename = (
            f"{document_type.value}_{document_id}.pdf"
        )

        DocumentStorageService.save_document(
            bidder_folder,
            stored_filename,
            file
        )

        #
        # Generate TXT only
        #

        pdf_path = bidder_folder / stored_filename

        DocumentService.process_pdf(
            pdf_path
        )

        #
        # Save database record
        #

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