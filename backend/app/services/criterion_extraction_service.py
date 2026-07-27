from datetime import datetime
from uuid import uuid4

from app.agents.criterion_extraction_agent import CriterionExtractionAgent
from app.domain.criterion import Criterion
from app.repositories.criterion_repository import CriterionRepository
from app.utils.storage_manager import StorageManager


class CriterionExtractionService:

    def __init__(self):
        self.agent = CriterionExtractionAgent()
        self.repository = CriterionRepository()

    def extract_from_tender(self, tender_id):

        document_folder = StorageManager.get_tender_documents_path(
            tender_id
        )

        nit_files = list(document_folder.glob("NIT*.txt"))

        if not nit_files:
            raise FileNotFoundError(
                "NIT text file not found."
            )

        text = nit_files[0].read_text(
            encoding="utf-8"
        )

        criteria = self.agent.extract(text)

        saved_criteria = []

        for item in criteria:

            criterion = Criterion(
                id=uuid4(),
                tender_id=tender_id,
                title=item["title"],
                description=item["description"],
                evidence_required=item["evidence_required"],
                mandatory=item["mandatory"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            self.repository.save(criterion)

            saved_criteria.append(criterion)

        return saved_criteria