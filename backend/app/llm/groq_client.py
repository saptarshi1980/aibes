import os

from groq import Groq

from app.llm.llm_client import LLMClient
from app.core.config import Config


class GroqClient(LLMClient):

    def __init__(self):
        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content