from app.core.config import Config
from app.llm.gemini_client import GeminiClient
from app.llm.groq_client import GroqClient
from app.llm.llm_client import LLMClient
from app.llm.huggingface_client import HuggingFaceClient
from app.llm.ollama_client import OllamaClient
from app.llm.ollama_client import OllamaClient


class LLMFactory:

    @staticmethod
    def get_client() -> LLMClient:

        provider = Config.LLM_PROVIDER.upper()

        if provider == "GROQ":
            return GroqClient()

        if provider == "GEMINI":
            return GeminiClient()
        
        elif provider == "HUGGINGFACE":
            return HuggingFaceClient()
        
        if Config.LLM_PROVIDER.upper() == "OLLAMA":
            return OllamaClient()

        raise ValueError(
            f"Unsupported LLM Provider: {provider}"
        )