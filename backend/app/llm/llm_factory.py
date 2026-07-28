from app.core.config import Config
from app.llm.gemini_client import GeminiClient
from app.llm.groq_client import GroqClient
from app.llm.llm_client import LLMClient


class LLMFactory:

    @staticmethod
    def get_client() -> LLMClient:

        provider = Config.LLM_PROVIDER.upper()

        if provider == "GROQ":
            return GroqClient()

        if provider == "GEMINI":
            return GeminiClient()

        raise ValueError(
            f"Unsupported LLM Provider: {provider}"
        )