class PromptManager:

    @staticmethod
    def criterion_extraction_prompt(document_text: str) -> str:

        return f"""
You are an expert in Government Tender Technical Evaluation.

The following text is ONLY ONE CHUNK of a tender document.

Your task is to extract ONLY the technical eligibility criteria that appear in THIS CHUNK.

Important Rules:

1. Extract ONLY technical eligibility/capability criteria and eligibility requirements.
2. Ignore commercial clauses.
3. Ignore payment terms.
4. Ignore delivery schedules.
5. Ignore warranty clauses.
6. Ignore general instructions unless they define eligibility.
7. Preserve the original wording as much as possible.
8. Do NOT invent information.
9. If this chunk contains no technical eligibility criterion, return:
[]
10. Return ONLY valid JSON.
11. Do NOT return markdown.
12. Do NOT explain anything.

Each criterion must have this format:

[
    {{
        "title": "",
        "description": "",
        "evidence_required": "",
        "mandatory": true
    }}
]

Text Chunk:

{document_text}
"""
