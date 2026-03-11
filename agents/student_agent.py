import arxiv
from core.llm_client import call_llm


def fetch_papers(topic: str, max_results: int = 5):
    """Fetch real papers from ArXiv, return context string and citations list"""

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    context = ""
    citations = []

    for i, result in enumerate(search.results()):
        authors = ", ".join(str(a) for a in result.authors[:3])
        year = result.published.year

        context += f"[{i+1}] {result.title} ({year})\n"
        context += f"Authors: {authors}\n"
        context += f"Abstract: {result.summary[:400]}\n\n"

        citations.append(
            f"[{i+1}] {authors} ({year}). {result.title}. "
            f"ArXiv: {result.entry_id}"
        )

    return context, citations


class StudentAgent:

    def generate_draft(self, topic, memory_context=None):

        # Fetch real papers from ArXiv
        print("🔍 Fetching real research papers from ArXiv...")
        try:
            rag_context, citations = fetch_papers(topic, max_results=5)
            citation_block = "\n".join(citations)
            rag_section = f"""
REAL RESEARCH PAPERS (you MUST cite these):
{rag_context}

REFERENCES TO USE EXACTLY:
{citation_block}
"""
        except Exception as e:
            print(f"⚠️ ArXiv fetch failed: {e}. Proceeding without RAG.")
            rag_section = ""
            citation_block = ""

        memory_section = ""
        if memory_context:
            memory_section = f"\nPrevious related work:\n{memory_context}\n"

        prompt = f"""
ROLE:
You are a graduate-level university student writing an academic paper.

OBJECTIVE:
Write a structured, evidence-based academic paper grounded in real research.

CONSTRAINTS:
- Formal tone
- Cite provided sources using [1], [2], [3] format
- Only make claims supported by the provided abstracts
- Clear headings
- No fluff
- Balanced perspective

TOPIC:
{topic}

{rag_section}

{memory_section}

REQUIRED STRUCTURE:
1. Introduction
2. 3-4 Core Sections (cite real papers throughout)
3. Challenges
4. Future Implications
5. Conclusion
6. References (use the exact references provided above)

IMPORTANT:
- Ensure the paper is fully completed
- Do not stop mid-sentence
- Always finish with a complete Conclusion and References section
- Every major claim must have a citation
"""

        return call_llm(prompt)

    def revise_draft(self, draft, feedback, topic=None):

        # Re-fetch papers for revision context if topic provided
        rag_section = ""
        if topic:
            try:
                rag_context, citations = fetch_papers(topic, max_results=3)
                citation_block = "\n".join(citations)
                rag_section = f"""
REAL RESEARCH CONTEXT (maintain these citations in revision):
{rag_context}

REFERENCES TO PRESERVE:
{citation_block}
"""
            except Exception as e:
                print(f"⚠️ ArXiv fetch failed during revision: {e}")

        prompt = f"""
ROLE:
You are revising your academic paper based on professor feedback.

OBJECTIVE:
Improve the paper while keeping all real citations intact.

RULES:
- Address all structural issues raised
- Strengthen weak arguments
- Maintain and expand citations from real sources
- Keep strong sections as-is
- No meta-commentary, just the paper

{rag_section}

ORIGINAL DRAFT:
{draft[:4000]}

PROFESSOR FEEDBACK:
{feedback}

Return the complete improved paper with all sections and references.
"""

        return call_llm(prompt)