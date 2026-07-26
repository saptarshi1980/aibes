from fastapi import FastAPI

from app.api.documents import router as document_router
from app.api.tenders import router as tender_router

app = FastAPI(
    title="AI Assisted Bid Evaluation System",
    version="1.0.0"
)

app.include_router(tender_router)
app.include_router(document_router)


@app.get("/")
def home():
    return {
        "project": "AIBES",
        "status": "Running"
    }