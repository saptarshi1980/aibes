from uuid import UUID

from fastapi import APIRouter

from app.repositories.criterion_repository import CriterionRepository
from app.services.document_retriever import DocumentRetriever

router = APIRouter(
    prefix="/api/v1/retriever",
    tags=["Retriever"]
)

retriever = DocumentRetriever()
criteria_repo = CriterionRepository()


@router.get("/{bidder_id}/{criterion_id}")
def retrieve(
    bidder_id: UUID,
    criterion_id: UUID
):

    criterion = criteria_repo.find_by_id(
        criterion_id
    )

    return {

        "retrieved_text": retriever.retrieve(
            bidder_id,
            criterion
        )

    }