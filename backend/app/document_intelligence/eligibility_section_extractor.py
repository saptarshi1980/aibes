import re


class EligibilitySectionExtractor:

    KEYWORDS = [

        "minimum eligibility",
        "eligibility criteria",
        "technical eligibility",
        "financial eligibility",
        "technical capability",
        "qualification criteria",
        "technical criteria",
        "financial criteria",
        "experience of executing",
        "similar nature of job",
        "similar completed works",
        "completion certificate",
        "work experience",
        "turnover",
        "oem",
        "emd",
        "solvency",
        "bid capacity",
        "documentary evidence",
        "technical and financial criteria"

    ]


    @classmethod
    def extract(cls, text: str):

        #
        # Split OCR text into paragraphs
        #

        paragraphs = re.split(r"\n\s*\n", text)

        selected = []

        for i, paragraph in enumerate(paragraphs):

            score = 0

            lower = paragraph.lower()

            for keyword in cls.KEYWORDS:

                if keyword in lower:
                    score += 1

            #
            # Strong paragraph
            #

            if score >= 2:

                #
                # include previous paragraph
                #

                if i > 0:
                    selected.append(paragraphs[i - 1])

                selected.append(paragraph)

                #
                # include next 8 paragraphs
                #

                for j in range(1, 9):

                    if i + j < len(paragraphs):
                        selected.append(paragraphs[i + j])

        #
        # Remove duplicates
        #

        cleaned = []

        seen = set()

        for p in selected:

            t = p.strip()

            if t and t not in seen:

                cleaned.append(t)

                seen.add(t)

        return "\n\n".join(cleaned)