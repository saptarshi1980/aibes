from google import genai

from app.core.config import Config
from app.llm.llm_client import LLMClient


class GeminiClient(LLMClient):

    def __init__(self):

        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.models.generate_content(
        model=Config.LLM_MODEL,
        contents=prompt
)

        return response.text