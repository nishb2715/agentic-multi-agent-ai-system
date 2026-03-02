from orchestrator import Orchestrator

if __name__ == "__main__":
    topic = input("Enter research topic: ")

    orchestrator = Orchestrator()
    final_paper = orchestrator.run(topic)

    print("\n===== FINAL PAPER =====\n")
    print(final_paper)