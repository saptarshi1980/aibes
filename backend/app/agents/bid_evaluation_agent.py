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

====================================================================

IMPORTANT EVALUATION RULES

1. Evaluate the SUBSTANCE of the submitted evidence, not merely the document title.

2. Documents with different names may be considered equivalent if they clearly satisfy the intent of the criterion.

Examples:
- Self Declaration
- Declaration
- Undertaking
- Affidavit
- Self Certification
- Certificate

3. Do NOT mark NOT_COMPLIED merely because the document title differs from the wording used in the tender.

4. If the submitted evidence clearly proves the requirement, mark COMPLIED.

5. Use NEEDS_MANUAL_REVIEW only when:
- the required document is missing,
- the evidence cannot be verified,
- the document is illegible,
- or the available evidence is insufficient.

6. When evaluating compliance, consider the actual CONTENT of the document more important than its title.

7. If a Self Declaration explicitly states that the bidder is not blacklisted or debarred, it shall be treated as a valid Undertaking for evaluating the non-blacklisting criterion.

8. If the bidder states that a supporting document is enclosed but that document is NOT present in the supplied bid text, do NOT assume compliance. Use NEEDS_MANUAL_REVIEW unless the available text itself proves compliance.

====================================================================

Criterion Title:
{criterion.title}

Criterion Description:
{criterion.description}

Evidence Required:
{criterion.evidence_required}

Mandatory:
{criterion.mandatory}

====================================================================

Relevant Extracts from Bidder Technical Bid

{bidder_text}

====================================================================

Instructions

1. Read the criterion carefully.

2. Read ONLY the supplied bidder text.

3. Decide whether the bidder satisfies the criterion.

4. Base your decision ONLY on the supplied text.

5. Quote the exact supporting text whenever available.

6. Do not invent evidence.

7. Return ONLY valid JSON.

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
        
        print("=" * 80)
        print("RAW RESPONSE FROM OLLAMA")
        print("=" * 80)
        print(response)
        print("=" * 80)

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