from fastapi import FastAPI

app = FastAPI(
    title="AI-Assisted Technical Bid Evaluation System",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project": "AIBES",
        "status": "Running"
    }