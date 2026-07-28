from uuid import UUID

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.domain.tender_document import TenderDocument
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.models.tender_document_model import TenderDocumentModel


class TenderDocumentRepository:

    def save(self, document: TenderDocument):

        with SessionLocal() as session:

            model = TenderDocumentModel(
                id=str(document.id),
                tender_id=str(document.tender_id),
                original_filename=document.original_filename,
                stored_filename=document.stored_filename,
                document_type=document.document_type.value,
                status=document.status.value,
                uploaded_at=document.uploaded_at
            )

            session.add(model)
            session.commit()

        return document

    def find_by_id(self, document_id: UUID):

        with SessionLocal() as session:

            model = session.get(
                TenderDocumentModel,
                str(document_id)
            )

            if model is None:
                return None

            return TenderDocument(
                id=UUID(model.id),
                tender_id=UUID(model.tender_id),
                original_filename=model.original_filename,
                stored_filename=model.stored_filename,
                document_type=DocumentType(model.document_type),
                status=DocumentStatus(model.status),
                uploaded_at=model.uploaded_at
            )

    def find_by_tender(self, tender_id: UUID):

        with SessionLocal() as session:

            rows = session.scalars(
                select(TenderDocumentModel).where(
                    TenderDocumentModel.tender_id == str(tender_id)
                )
            ).all()

            return [

                TenderDocument(
                    id=UUID(row.id),
                    tender_id=UUID(row.tender_id),
                    original_filename=row.original_filename,
                    stored_filename=row.stored_filename,
                    document_type=DocumentType(row.document_type),
                    status=DocumentStatus(row.status),
                    uploaded_at=row.uploaded_at
                )

                for row in rows

            ]