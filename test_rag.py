# test_rag.py
from agents.student_agent import fetch_papers

context, citations = fetch_papers("Blockchain in Finance", max_results=3)
print("=== CONTEXT ===")
print(context)
print("=== CITATIONS ===")
for c in citations:
    print(c)