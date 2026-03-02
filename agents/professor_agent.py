from core.llm_client import call_llm


class ProfessorAgent:

    def review(self, draft, round_number=1):

        if round_number == 1:
            strictness_note = "Be constructively critical."
        else:
            strictness_note = "If major issues are resolved, APPROVE."

        prompt = f"""
        ROLE:
        You are a senior academic professor.

        TASK:
        Evaluate the paper using this rubric:

        1. Structure (score 1–10)
        2. Clarity (score 1–10)
        3. Depth (score 1–10)
        4. Suggestions for improvement

        {strictness_note}

        Conclude with exactly one word:
        APPROVED
        or
        REVISE

        PAPER:
        {draft[:4000]}
        """

        return call_llm(prompt)

    def score_quality(self, draft):
        prompt = f"""
        Rate this academic paper out of 10 for overall academic quality.
        Return only a number.

        PAPER:
        {draft[:4000]}
        """

        return call_llm(prompt)