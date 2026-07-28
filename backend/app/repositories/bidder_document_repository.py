from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.domain.bidder_document import BidderDocument
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.models.bidder_document_model import BidderDocumentModel


class BidderDocumentRepository:

    def save(self, document: BidderDocument):

        with SessionLocal() as session:

            model = BidderDocumentModel(
                id=str(document.id),
                bidder_id=str(document.bidder_id),
                original_filename=document.original_filename,
                stored_filename=document.stored_filename,
                document_type=document.document_type.value,
                status=document.status.value,
                uploaded_at=document.uploaded_at
            )

            session.add(model)
            session.commit()

        return document

    def find_by_bidder(self, bidder_id: UUID):

        with SessionLocal() as session:

            rows = session.scalars(
                select(BidderDocumentModel).where(
                    BidderDocumentModel.bidder_id == str(bidder_id)
                )
            ).all()

            return [

                BidderDocument(
                    id=UUID(row.id),
                    bidder_id=UUID(row.bidder_id),
                    original_filename=row.original_filename,
                    stored_filename=row.stored_filename,
                    document_type=DocumentType(row.document_type),
                    status=DocumentStatus(row.status),
                    uploaded_at=row.uploaded_at
                )

                for row in rows

            ]
            
    def find_by_document_type(
    self,
    bidder_id: UUID,
    document_type: DocumentType
):

        with SessionLocal() as session:

            model = session.scalar(

                select(BidderDocumentModel).where(
                    BidderDocumentModel.bidder_id == str(bidder_id),
                    BidderDocumentModel.document_type == document_type.value
                )

            )

            if model is None:
                return None

            return BidderDocument(
                id=UUID(model.id),
                bidder_id=UUID(model.bidder_id),
                original_filename=model.original_filename,
                stored_filename=model.stored_filename,
                document_type=DocumentType(model.document_type),
                status=DocumentStatus(model.status),
                uploaded_at=model.uploaded_at
            )