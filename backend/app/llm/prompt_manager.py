class PromptManager:

    @staticmethod
    def criterion_extraction_prompt(document_text: str) -> str:

        return f"""
You are an expert in public procurement.

Read the following tender document and extract every technical eligibility criterion.

Instructions:

Instructions:

1. Extract every technical qualification criterion.
2. Ignore commercial clauses.
3. Ignore payment terms.
4. Ignore general instructions unless they are mandatory eligibility conditions.
5. Return ONLY valid JSON.
6. Do not include markdown.
7. Do not explain anything.
8. Preserve the original clause number exactly as it appears in the tender.
9. Do NOT renumber the criteria.
10. If no clause number exists, leave criterion_number as an empty string.

JSON Format:

[
    {{
    
        "title": "",
        "description": "",
        "evidence_required": "",
        "keywords": [],
        "mandatory": true
    }}
]

Tender Document:

{document_text}
"""