from app.repositories.bidder_repository import BidderRepository
from app.repositories.bidder_document_repository import BidderDocumentRepository
from app.repositories.evaluation_result_repository import EvaluationResultRepository

from app.rag.vector_store import VectorStore
from app.utils.storage_manager import StorageManager

import shutil
import os


class BidderDeleteService:

    def __init__(self):

        self.bidder_repository = BidderRepository()

        self.document_repository = BidderDocumentRepository()

        self.result_repository = EvaluationResultRepository()

        self.vector_store = VectorStore()

    def delete_bidder(
        self,
        bidder_id
    ):

        bidder = self.bidder_repository.find_by_id(
            bidder_id
        )

        if bidder is None:

            raise ValueError(
                "Bidder not found."
            )

        #
        # Delete evaluation results
        #

        self.result_repository.delete_by_bidder(
            bidder.id
        )

        #
        # Delete document records
        #

        self.document_repository.delete_by_bidder(
            bidder.id
        )

        #
        # Delete bidder folder
        #

        bidder_folder = StorageManager.get_bidder_documents_path(

            bidder.tender_id,

            bidder.bidder_name

        )

        if os.path.exists(bidder_folder):

            shutil.rmtree(bidder_folder)

        #
        # Delete embeddings
        #

        self.vector_store.delete(
            bidder.id
        )

        #
        # Delete bidder record
        #

        self.bidder_repository.delete(
            bidder.id
        )

        return {

            "message": "Bidder deleted successfully."

        }