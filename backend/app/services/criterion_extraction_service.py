from datetime import datetime
from uuid import uuid4
from app.utils.text_chunker import TextChunker
from app.agents.criterion_extraction_agent import CriterionExtractionAgent
from app.document_intelligence.eligibility_section_extractor import (
    EligibilitySectionExtractor,
)
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

        nit_files = list(
            document_folder.glob("NIT*.txt")
        )

        if not nit_files:
            raise FileNotFoundError(
                "NIT text file not found."
            )

        #
        # Read OCR text
        #

        text = nit_files[0].read_text(
            encoding="utf-8"
        )

        #
        # Extract only the eligibility section
        #

        eligibility_text = (
            EligibilitySectionExtractor.extract(
                text
            )
        )

        #
        # Save extracted section for debugging
        #

        debug_file = (
            document_folder /
            "eligibility_preview.txt"
        )

        debug_file.write_text(
            eligibility_text,
            encoding="utf-8"
        )

        print("=" * 80)
        print(
            "Full OCR Length :",
            len(text)
        )
        print(
            "Eligibility Length :",
            len(eligibility_text)
        )
        print("=" * 80)

        #
        # First run AI extraction.
        # Old criteria remain untouched if AI fails.
        #

        chunks = TextChunker.chunk_text(
        eligibility_text
        )

        print(f"\nTotal Chunks : {len(chunks)}")

        all_criteria = []

        for index, chunk in enumerate(chunks):

            print("=" * 80)
            print(f"Processing Chunk {index + 1}/{len(chunks)}")
            print(f"Chunk Length : {len(chunk)}")
            print("=" * 80)
            
            #
# Save each chunk for debugging
#

            chunk_file = (
                document_folder /
                f"chunk_{index + 1}.txt"
            )

            chunk_file.write_text(
                chunk,
                encoding="utf-8"
            )


            criteria = self.agent.extract(
                chunk,
                chunk_number=index + 1
            )

            if criteria:
                all_criteria.extend(criteria)

        #
        # AI succeeded.
        # Remove previous criteria.
        #

        self.repository.delete_by_tender(
            tender_id
        )

        saved_criteria = []

        for item in all_criteria:

            criterion = Criterion(

                id=uuid4(),

                tender_id=tender_id,

                title=item["title"],

                description=item["description"],

                evidence_required=item[
                    "evidence_required"
                ],

                mandatory=item["mandatory"],

                created_at=datetime.now(),

                updated_at=datetime.now()

            )

            self.repository.save(
                criterion
            )

            saved_criteria.append(
                criterion
            )

        return saved_criteria