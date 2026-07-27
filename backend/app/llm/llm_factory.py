from app.core.config import Config
from app.llm.groq_client import GroqClient
from app.llm.llm_client import LLMClient


class LLMFactory:

    @staticmethod
    def get_client() -> LLMClient:

        if Config.LLM_PROVIDER.upper() == "GROQ":
            return GroqClient()

        raise ValueError(
            f"Unsupported LLM Provider: {Config.LLM_PROVIDER}"
        )