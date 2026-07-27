from fastapi import APIRouter

from app.llm.llm_factory import LLMFactory

router = APIRouter(
    prefix="/api/v1/llm",
    tags=["LLM"]
)


@router.get("/test")
def test_llm():

    client = LLMFactory.get_client()

    response = client.generate(
        "Reply with exactly these two words: Groq Connected"
    )

    return {
        "response": response
    }