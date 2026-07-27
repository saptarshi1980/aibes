from abc import ABC, abstractmethod


class LLMClient(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to the LLM and returns the response.
        """
        pass