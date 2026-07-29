from ollama import chat

from app.core.config import Config
from app.llm.llm_client import LLMClient


class OllamaClient(LLMClient):

    def generate(
        self,
        prompt: str
    ) -> str:

        response = chat(
            model=Config.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]