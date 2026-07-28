import json

from app.llm.llm_factory import LLMFactory


class BidEvaluationAgent:

    def __init__(self):

        self.llm = LLMFactory.get_client()

    def evaluate(
        self,
        criterion,
        bidder_text
    ):

        prompt = f"""
You are an expert technical bid evaluation officer.

Your task is to determine whether the bidder satisfies the tender criterion.

--------------------------------------------------------

Criterion Title:
{criterion.title}

Criterion Description:
{criterion.description}

Evidence Required:
{criterion.evidence_required}

Mandatory:
{criterion.mandatory}

--------------------------------------------------------

Technical Bid

{bidder_text}

--------------------------------------------------------

Instructions:

1. Read the criterion carefully.

2. Examine the technical bid.

3. Decide whether the criterion is satisfied.

4. Quote the relevant supporting text if found.

5. Respond ONLY as JSON.

Allowed status values:

COMPLIED
PARTIALLY_COMPLIED
NOT_COMPLIED
NOT_FOUND
NEEDS_MANUAL_REVIEW

Return exactly:

{{
    "status": "...",
    "confidence": 0.95,
    "matched_text": "...",
    "remarks": "..."
}}

Do not write markdown.

Do not explain anything outside the JSON.
"""

        response = self.llm.generate(prompt)

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        if response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        return json.loads(response)