from pathlib import Path
from uuid import UUID

from app.repositories.bidder_repository import BidderRepository
from app.rag.index_service import IndexService
from app.utils.storage_manager import StorageManager


class BidderIndexService:

    def __init__(self):

        self.bidder_repository = BidderRepository()

        self.index_service = IndexService()

    def generate_index(
        self,
        bidder_id: UUID
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

        txt_files = list(
            bidder_folder.glob("*.txt")
        )

        if len(txt_files) == 0:

            raise ValueError(
                "Technical Bid text not found."
            )

        #
        # There should be only one txt
        #

        txt_path = txt_files[0]

        self.index_service.build_index(

            bidder.id,

            str(txt_path)

        )

        return {

            "message": "Embeddings generated successfully."

        }