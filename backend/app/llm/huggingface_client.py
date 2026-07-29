from openai import OpenAI

from app.core.config import Config
from app.llm.llm_client import LLMClient


class HuggingFaceClient(LLMClient):

    def __init__(self):

        self.client = OpenAI(
            api_key=Config.HF_API_KEY,
            base_url="https://router.huggingface.co/v1"
        )

    def generate(
        self,
        prompt: str
    ) -> str:

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