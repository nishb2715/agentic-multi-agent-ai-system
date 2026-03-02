# 🧠 Aether: Multi-Agent Agentic Research System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![LLM](https://img.shields.io/badge/LLM-Groq--Llama--3.1-orange.svg)

Aether is a bounded, multi-agent Agentic AI system designed to autonomously draft, critique, revise, and evaluate research papers. By implementing structured orchestration and reflective reasoning loops, Aether moves beyond simple prompt engineering into the realm of **Production-Aware Agentic Design**.

---

## 🚀 Project Overview

Aether demonstrates controlled AI autonomy through a modular architecture where specialized agents collaborate to achieve high-quality academic outputs. 

### Core Components:
* 🎓 **Student Agent**: Generates structured academic drafts based on initial prompts.
* 👨‍🏫 **Professor Agent**: Provides rubric-based critiques and evaluations.
* 🧭 **Orchestrator**: The "brain" of the system—manages state, iteration loops, and termination.
* 💾 **Memory Layer**: A lightweight persistence layer for historical context.
* 📊 **Execution Logger**: Captures metadata, quality scores, and latency for observability.
* 🤖 **Telegram Interface**: Provides a real-time, user-facing interaction layer.

---

## 🏗 System Architecture

Aether utilizes a **centralized orchestration** pattern to manage the communication between agents and external APIs.

```mermaid
graph TD
    User[User via Telegram] --> Orchestrator
    Orchestrator --> Memory[Memory Layer - JSON]
    Orchestrator --> Student[Student Agent]
    Student --> Prof[Professor Agent]
    Prof --> Eval{Score >= Threshold?}
    Eval -- No (Iterate) --> Student
    Eval -- Yes / Max Loops --> Final[Final Paper]
    Final --> Logger[Execution Logger]
    Final --> User
    
    subgraph Inference Backend
    Student -.-> Groq[Groq LLM API]
    Prof -.-> Groq
    end
🧩 What Makes This "Agentic"?
Unlike standard LLM chains, Aether introduces sophisticated behaviors that define true agentic systems:

Role Specialization: Agents have distinct personas and constraints.

Reflective Reasoning: The system critiques its own work and performs targeted revisions.

Bounded Autonomy: Logic-gated loops (max 2 iterations) prevent infinite loops and control costs.

State Management: The Orchestrator tracks the evolution of the document across rounds.

Observability: Every decision and score is logged for post-run auditing.

🔁 Execution Flow
Input: User submits a topic via Telegram.

Context: Orchestrator retrieves relevant keywords from the Memory Layer.

Drafting: Student Agent generates the initial version.

Critique: Professor Agent evaluates the draft against a rubric.

Iteration: If feedback is "REVISE", the Student Agent receives the critique and updates the paper.

Termination: The loop ends when the Professor approves or the 2-iteration cap is reached.

Finalization: The system logs metadata, updates memory, and delivers the final result.

📊 Execution Metadata
Every run is captured in a timestamped JSON log, including:
| Metric | Description |
| :--- | :--- |
| Quality Score | Numerical evaluation from the Professor Agent |
| Iteration Count | Number of revision rounds performed |
| Latency | Time taken for full execution |
| Memory Sync | Keywords extracted for future runs |
| Model | The specific Groq model used (e.g., Llama-3.1-8b) |

🛠 Installation & Setup
1. Clone the Repository
Bash
git clone [https://github.com/your-username/aether-agentic-ai.git](https://github.com/your-username/aether-agentic-ai.git)
cd aether-agentic-ai
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Environment Configuration
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
4. Run the System
Bash
python -m bot.student_bot
⚠️ Known Limitations
No Tool Use: Currently does not perform live web searches (No RAG).

Keyword Memory: Uses basic JSON keyword storage rather than a Vector Database.

Stateless Agents: Individual agents do not "remember" sessions; the Orchestrator handles state.

🏗 Scalability Roadmap
[ ] Vector Memory: Implement FAISS or Pinecone for semantic retrieval.

[ ] RAG Integration: Add a Search Tool for real-time data gathering.

[ ] Multi-Model Routing: Use larger models (Llama-3.1-70b) for evaluation and smaller ones for drafting.

[ ] Containerization: Full Docker support for cloud deployment.

💡 Use Cases
Academic Drafting: Rapidly generating initial literature reviews.

Enterprise QA: Autonomous quality assurance for technical documentation.

Legal Memos: Drafting and internal peer-reviewing of legal summaries.
