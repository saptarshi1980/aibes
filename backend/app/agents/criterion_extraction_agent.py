from urllib import response

from app.llm.llm_factory import LLMFactory
from app.llm.prompt_manager import PromptManager
import json

class CriterionExtractionAgent:

    def __init__(self):
        self.llm = LLMFactory.get_client()

    def extract(self, document_text: str) -> str:

        prompt = PromptManager.criterion_extraction_prompt(
        document_text
    )

        response = self.llm.generate(prompt)

        return json.loads(response)