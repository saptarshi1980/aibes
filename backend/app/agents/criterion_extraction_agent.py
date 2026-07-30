import json
from pathlib import Path

from app.llm.llm_factory import LLMFactory
from app.llm.prompt_manager import PromptManager


class CriterionExtractionAgent:

    def __init__(self):

        self.llm = LLMFactory.get_client()

    def extract(
        self,
        document_text: str,
        chunk_number: int = 1
    ):

        prompt = PromptManager.criterion_extraction_prompt(
            document_text
        )

        print("=" * 80)
        print(f"Processing Chunk {chunk_number}")
        print("Sending prompt to Ollama...")
        print("Prompt Length:", len(prompt))
        print("=" * 80)

        response = self.llm.generate(
            prompt
        )

        #
        # Save raw response
        #

        debug_folder = Path("storage/debug")

        debug_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        (
            debug_folder /
            f"criterion_chunk_{chunk_number}.json"
        ).write_text(
            response,
            encoding="utf-8"
        )

        print("=" * 80)
        print("LLM Response Length:", len(response))
        print("=" * 80)

        print(response[:4000])

        print("=" * 80)

        #
        # Clean markdown if Ollama returns it
        #

        response = response.strip()

        if response.startswith("```json"):
            response = response.replace(
                "```json",
                "",
                1
            )

        if response.startswith("```"):
            response = response.replace(
                "```",
                "",
                1
            )

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        #
        # Parse JSON
        #

        try:

            return json.loads(
                response
            )

        except json.JSONDecodeError as ex:

            print("\n")
            print("=" * 80)
            print("JSON Parsing Failed")
            print("=" * 80)

            print(response)

            raise ValueError(

                f"""
Ollama did not return valid JSON.

Chunk : {chunk_number}

Check:

storage/debug/criterion_chunk_{chunk_number}.json
"""

            ) from ex