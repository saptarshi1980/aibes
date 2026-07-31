from pathlib import Path
from uuid import UUID


class BidderStatusService:

    def embedding_status(
        self,
        bidder_id: UUID
    ):

        folder = Path("vector_db") / str(bidder_id)

        generated = (
            (folder / "index.faiss").exists()
            and
            (folder / "index.pkl").exists()
        )

        return {
            "generated": generated
        }