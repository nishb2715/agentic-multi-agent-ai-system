from core.llm_client import call_llm


class StudentAgent:

    def generate_draft(self, topic, memory_context=None):

        memory_section = ""
        if memory_context:
            memory_section = f"\nPrevious related work:\n{memory_context}\n"

        prompt = f"""
        ROLE:
        You are a graduate-level university student.

        OBJECTIVE:
        Write a structured academic paper.

        CONSTRAINTS:
        - Formal tone
        - Evidence-based reasoning
        - Clear headings
        - No fluff
        - Balanced perspective

        TOPIC:
        {topic}

        {memory_section}

        REQUIRED STRUCTURE:
        1. Introduction
        2. 3–4 Core Sections
        3. Challenges
        4. Future Implications
        5. Conclusion


        Ensure the paper is fully completed.
        Do not stop mid-sentence.
        Always finish with a complete Conclusion section.

        
        """

        return call_llm(prompt)

    def revise_draft(self, draft, feedback):

        prompt = f"""
        ROLE:
        You are revising your academic paper.

        OBJECTIVE:
        Improve based on professor feedback.

        RULES:
        - Address structural issues
        - Strengthen weak arguments
        - Maintain strong sections
        - No commentary

        ORIGINAL DRAFT:
        {draft[:4000]}

        FEEDBACK:
        {feedback}

        Return the improved full paper.
        """

        return call_llm(prompt)