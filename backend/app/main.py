from fastapi import FastAPI

from app.api.documents import router as document_router
from app.api.tenders import router as tender_router
from app.api.tender_documents import router as tender_document_router
from uuid import UUID
from app.api.criteria import router as criteria_router
from app.api.document_intelligence import router as document_intelligence_router
from app.api.llm_test import router as llm_router
from app.api.ai_test import router as ai_test_router
from app.database.base import Base
from app.database.connection import engine

from app.models.tender_model import TenderModel


app = FastAPI(
    title="AI Assisted Bid Evaluation System",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

app.include_router(tender_router)
app.include_router(document_router)
app.include_router(tender_document_router)
app.include_router(criteria_router)
app.include_router(document_intelligence_router)
app.include_router(llm_router)
app.include_router(ai_test_router)

@app.get("/")
def home():
    return {
        "project": "AIBES",
        "status": "Running"
    }

