import json
import logging

from app.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)


class BidEvaluationAgent:

    def __init__(self):

        self.llm = LLMFactory.get_client()

    def evaluate(
        self,
        criterion,
        bidder_text
    ):

        print("=" * 80)
        print("Retriever returned:", len(bidder_text), "characters")
        print("=" * 80)
        print(bidder_text[:1000])
        print("=" * 80)

        prompt = f"""
You are an expert Technical Bid Evaluation Officer.

Your responsibility is to determine whether the bidder satisfies ONE tender criterion.

====================================================

Criterion Title:
{criterion.title}

Criterion Description:
{criterion.description}

Evidence Required:
{criterion.evidence_required}

Mandatory:
{criterion.mandatory}

====================================================

Relevant Extracts from Bidder Technical Bid

{bidder_text}

====================================================

Instructions

1. Read the criterion carefully.

2. Read ONLY the supplied bidder text.

3. Decide whether the bidder satisfies the criterion.

4. Quote the exact supporting text whenever available.

5. If evidence is insufficient, do NOT assume compliance.

6. Return ONLY JSON.

Allowed status values

COMPLIED
PARTIALLY_COMPLIED
NOT_COMPLIED
NOT_FOUND
NEEDS_MANUAL_REVIEW

Return EXACTLY

{{
    "status":"COMPLIED",
    "confidence":0.95,
    "matched_text":"...",
    "remarks":"..."
}}

Do NOT return markdown.

Do NOT explain anything.

Return JSON only.
"""

        logger.info("Sending prompt to Gemini...")

        response = self.llm.generate(prompt)

        logger.info("Gemini response received.")

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        if response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:

            result = json.loads(response)

        except Exception:

            logger.exception("Invalid JSON received from Gemini")
            logger.error(response)

            raise ValueError(
                "Gemini returned invalid JSON."
            )

        required_fields = [
            "status",
            "confidence",
            "matched_text",
            "remarks"
        ]

        for field in required_fields:

            if field not in result:

                raise ValueError(
                    f"Gemini response missing field '{field}'."
                )

        logger.info("Evaluation completed successfully.")

        return result