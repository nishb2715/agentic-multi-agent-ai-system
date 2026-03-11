import arxiv
from core.llm_client import call_llm


def fetch_papers_for_review(topic: str, max_results: int = 3):
    """Fetch real papers to give professor grounded review context"""

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    context = ""

    for i, result in enumerate(search.results()):
        authors = ", ".join(str(a) for a in result.authors[:3])
        year = result.published.year

        context += f"[{i+1}] {result.title} ({year})\n"
        context += f"Authors: {authors}\n"
        context += f"Abstract: {result.summary[:400]}\n\n"

    return context


class ProfessorAgent:

    def review(self, draft, round_number=1, topic=None):

        if round_number == 1:
            strictness_note = "Be constructively critical. Point out gaps clearly."
        else:
            strictness_note = "If major issues are resolved, you MUST APPROVE. Be generous on round 2."

        # Fetch real papers so professor reviews against actual literature
        rag_section = ""
        if topic:
            try:
                print("🔍 Professor fetching real papers for grounded review...")
                rag_context = fetch_papers_for_review(topic, max_results=3)
                rag_section = f"""
REAL RESEARCH CONTEXT:
The following are real published papers on this topic.
Use these to evaluate whether the student's claims are accurate and well-grounded.

{rag_context}
"""
            except Exception as e:
                print(f"⚠️ ArXiv fetch failed for professor review: {e}")

        prompt = f"""
ROLE:
You are a senior academic professor conducting a formal paper review.

TASK:
Evaluate the submitted paper using this rubric:

1. Structure (score 1-10)
2. Clarity (score 1-10)
3. Depth (score 1-10)
4. Citation Quality — are claims grounded in real sources?
5. Accuracy — do claims align with the real research provided?
6. Suggestions for improvement

{strictness_note}

{rag_section}

PAPER TO REVIEW:
{draft[:4000]}

End your review with exactly one of these two words on its own line:
APPROVED
or
REVISE
"""

        return call_llm(prompt)

    def score_quality(self, draft):

        prompt = f"""
Rate this academic paper out of 10 for overall academic quality.
Consider structure, clarity, depth, and citation quality.
Return only a single number between 1 and 10. Nothing else.

PAPER:
{draft[:4000]}
"""

        return call_llm(prompt)