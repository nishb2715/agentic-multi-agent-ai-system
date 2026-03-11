# test_orchestrator.py
from orchestrator import Orchestrator

orc = Orchestrator()
result = orc.run("Blockchain in Finance")

print("\n=== APPROVAL STATUS ===")
print(result["execution_metadata"]["approval_status"])

print("\n=== FINAL PAPER PREVIEW ===")
print(result["final_paper"][:500])