from pathlib import Path

from fastapi import APIRouter

from app.agents.criterion_extraction_agent import CriterionExtractionAgent

router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI Test"]
)


@router.post("/extract-criteria")
def extract_criteria():

    txt_file = Path(
        r"D:/AIBES/backend/storage/tenders/17c6ac63-1a46-4813-9363-5f23b1725cb9_DPL_ITC_SMS_200/tender_documents/NIT_581d6732-6625-4ff5-894d-345b00bc6fc0.txt"
    )

    document_text = txt_file.read_text(
        encoding="utf-8"
    )
    
    print("=" * 80)
    print(document_text[:5000])
    print("=" * 80)

    agent = CriterionExtractionAgent()

    response = agent.extract(document_text)

    return response