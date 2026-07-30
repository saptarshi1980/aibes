from datetime import datetime
from uuid import UUID, uuid4
import os
from app.rag.rag_retriever import RAGRetriever
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

        self.retriever = RAGRetriever()
    
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

        # ---------------------------------------------------
        # Replace existing Technical Bid if one already exists
        # ---------------------------------------------------

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
                # Delete extracted TXT
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

                try:

                    self.retriever.delete_embeddings(
                        bidder_id
                    )

                except Exception as ex:

                    print(
                        "Vector deletion failed :",
                        ex
                    )

                #
                # Delete DB record
                #

                self.repository.delete(
                    existing.id
                )

        #
        # Save new document
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