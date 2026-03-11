import os
import json
import time
from datetime import datetime

from agents.student_agent import StudentAgent
from agents.professor_agent import ProfessorAgent
from config import MODEL_NAME, MAX_TOKENS


class Orchestrator:

    def __init__(self):
        self.student = StudentAgent()
        self.professor = ProfessorAgent()
        self.memory_file = "memory/memory_store.json"

    def run(self, topic):

        start_time = time.time()
        rounds_used = 1
        approval_status = "MAX_REVISIONS_REACHED"  # default, overwritten if approved

        print("→ Checking memory...")
        memory_context = self.get_memory(topic)

        log_data = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "draft_round_1": None,
            "feedback_round_1": None,
            "draft_round_2": None,
            "feedback_round_2": None,
            "final_paper": None,
            "execution_metadata": {
                "model": MODEL_NAME,
                "max_tokens": MAX_TOKENS,
                "rounds_used": None,
                "execution_time_seconds": None,
                "quality_score": None,
                "approval_status": None
            }
        }

        try:
            # ── ROUND 1 ──────────────────────────────────────────
            print("→ Student fetching real papers + drafting...")
            draft1 = self.student.generate_draft(topic, memory_context)

            if not draft1 or not draft1.strip():
                return "Error: Student agent returned empty draft."

            if not draft1.strip().endswith((".", "!", "?")):
                print("→ Incomplete draft detected. Regenerating...")
                draft1 = self.student.generate_draft(topic, memory_context)

            log_data["draft_round_1"] = draft1

            print("→ Professor reviewing (Round 1)...")
            feedback1 = self.professor.review(draft1, round_number=1, topic=topic)
            log_data["feedback_round_1"] = feedback1

            if feedback1 and "APPROVED" in feedback1:
                final_paper = draft1
                approval_status = "APPROVED"
                rounds_used = 1

            else:
                rounds_used = 2

                # ── ROUND 2 ──────────────────────────────────────
                print("→ Student revising with RAG context...")
                draft2 = self.student.revise_draft(draft1, feedback1, topic=topic)

                if not draft2 or not draft2.strip():
                    print("→ Empty revision returned. Using draft1 as fallback.")
                    draft2 = draft1

                if not draft2.strip().endswith((".", "!", "?")):
                    print("→ Incomplete revision detected. Regenerating...")
                    draft2 = self.student.revise_draft(draft1, feedback1, topic=topic)

                log_data["draft_round_2"] = draft2

                print("→ Professor reviewing (Round 2)...")
                feedback2 = self.professor.review(draft2, round_number=2, topic=topic)
                log_data["feedback_round_2"] = feedback2

                final_paper = draft2

                if feedback2 and "APPROVED" in feedback2:
                    approval_status = "APPROVED"
                else:
                    approval_status = "MAX_REVISIONS_REACHED"

        except Exception as e:
            return f"System error occurred: {e}"

        print("→ Scoring final paper...")

        # Quality score
        try:
            raw_score = self.professor.score_quality(final_paper)
            score_digits = ''.join(filter(str.isdigit, raw_score))
            quality_score = int(score_digits[:2]) if score_digits else None
            # cap to 10 in case model returns "10" as "10" or garbage like "108"
            if quality_score and quality_score > 10:
                quality_score = 10
        except Exception:
            quality_score = None

        execution_time = round(time.time() - start_time, 2)

        # Update log
        log_data["final_paper"] = final_paper
        log_data["execution_metadata"]["rounds_used"] = rounds_used
        log_data["execution_metadata"]["execution_time_seconds"] = execution_time
        log_data["execution_metadata"]["quality_score"] = quality_score
        log_data["execution_metadata"]["approval_status"] = approval_status

        self.save_log(log_data)
        self.update_memory(topic, final_paper)

        print("\n===== EXECUTION SUMMARY =====")
        print("Rounds Used      :", rounds_used)
        print("Approval Status  :", approval_status)
        print("Quality Score    :", quality_score)
        print("Execution Time(s):", execution_time)

        return log_data


    def save_log(self, data):
        os.makedirs("logs", exist_ok=True)
        filename = f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Log saved to:", filename)


    def get_memory(self, topic):

        if not os.path.exists(self.memory_file):
            return None

        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return None
                memory = json.loads(content)
        except Exception:
            return None

        topic_keywords = topic.lower().split()

        for entry in memory:
            stored_keywords = entry["topic"].lower().split()
            if any(word in stored_keywords for word in topic_keywords):
                return entry["summary"]

        return None


    def update_memory(self, topic, final_paper):

        os.makedirs("memory", exist_ok=True)

        summary = final_paper[:1000]

        entry = {
            "topic": topic,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }

        memory = []

        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        memory = json.loads(content)
            except Exception:
                memory = []

        memory.append(entry)
        memory = memory[-10:]  # keep last 10 only

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4)