from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from app.api.bidder_status import router as bidder_status_router
from app.models.tender_model import TenderModel
from app.models.bidder_model import BidderModel
from app.api.bidders import router as bidder_router
from app.models.bidder_document_model import BidderDocumentModel
from app.api.bidder_documents import router as bidder_document_router
from app.api.bidder_delete import router as bidder_delete_router
from app.models.criterion_model import CriterionModel
from app.models.evaluation_result_model import EvaluationResultModel
from app.api.evaluation import router as evaluation_router
from app.api.retriever import router as retriever_router
from app.api.bidder_index import router as bidder_index_router
from app.api.evaluation_report import router as evaluation_report_router
from app.api.tender_report import router as tender_report_router
from app.api.tender_excel_report import router as tender_excel_router
from app.api.tender_pdf_view import router as tender_pdf_view_router

app = FastAPI(
    title="AI Assisted Bid Evaluation System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(tender_router)
app.include_router(document_router)
app.include_router(tender_document_router)
app.include_router(criteria_router)
app.include_router(document_intelligence_router)
app.include_router(llm_router)
app.include_router(ai_test_router)
app.include_router(bidder_router)
app.include_router(
    bidder_document_router
)
app.include_router(
    evaluation_router
)
app.include_router(retriever_router)
app.include_router(
    bidder_index_router
)
app.include_router(
    bidder_status_router
)

app.include_router(
    bidder_delete_router
)

app.include_router(
    evaluation_report_router
)

app.include_router(tender_report_router)
app.include_router(
    tender_excel_router
)

app.include_router(
    tender_pdf_view_router
)

@app.get("/")
def home():
    return {
        "project": "AIBES",
        "status": "Running"
    }

