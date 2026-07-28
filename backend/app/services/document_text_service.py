from pathlib import Path
from uuid import UUID

from app.enums.document_type import DocumentType
from app.repositories.bidder_document_repository import (
    BidderDocumentRepository
)
from app.repositories.bidder_repository import BidderRepository
from app.utils.storage_manager import StorageManager


class DocumentTextService:

    def __init__(self):

        self.bidder_repository = BidderRepository()

        self.document_repository = (
            BidderDocumentRepository()
        )

    def get_bidder_text(
        self,
        bidder_id: UUID
    ) -> str:

        bidder = self.bidder_repository.find_by_id(
            bidder_id
        )

        if bidder is None:
            raise ValueError(
                "Bidder not found."
            )

        document = (
            self.document_repository.find_by_document_type(
                bidder_id,
                DocumentType.TECHNICAL_BID
            )
        )

        if document is None:
            raise ValueError(
                "Technical bid not uploaded."
            )

        bidder_folder = (
            StorageManager.get_bidder_documents_path(
                bidder.tender_id,
                bidder.bidder_name
            )
        )

        txt_file = (
            bidder_folder /
            Path(document.stored_filename).with_suffix(".txt")
        )

        if not txt_file.exists():
            raise FileNotFoundError(
                "Technical bid text file not found."
            )

        return txt_file.read_text(
            encoding="utf-8"
        )