# 🧠 Aether: Multi-Agent Agentic Research System

Aether is a bounded multi-agent Agentic AI system that autonomously drafts, critiques, revises, and evaluates research papers using structured orchestration.

This project demonstrates controlled AI autonomy, reflective reasoning loops, modular agent design, and production-aware system architecture — moving beyond simple prompt engineering into structured agentic systems design.

---

## 🚀 Project Overview

Aether implements a multi-agent architecture consisting of:

- 🎓 **Student Agent** – Generates structured academic drafts  
- 👨‍🏫 **Professor Agent** – Critiques drafts using a rubric-based evaluation  
- 🧭 **Orchestrator** – Manages iteration, state, and termination control  
- 💾 **Memory Layer** – Stores past topic summaries  
- 📊 **Execution Logger** – Tracks quality score, latency, and metadata  
- 🤖 **Telegram Interface** – Real-time user interaction layer  
- ☁️ **Groq LLM API** – Cost-optimized inference backend  

The system enforces **bounded autonomy** with a maximum of two reflection iterations to ensure safety, predictability, and cost control.

---

## 🧩 What Makes This Agentic?

Unlike single-shot LLM prompts, Aether introduces:

- Role-specialized agents
- Structured reflective loops
- Goal-directed iteration
- State tracking
- Bounded termination logic
- Observability through execution logs
- Persistent memory integration

This elevates the system beyond simple prompt chaining into a controlled agentic architecture.

---

## 🔁 Execution Flow

1. User submits research topic via Telegram  
2. Orchestrator retrieves relevant memory context  
3. Student Agent generates draft  
4. Professor Agent evaluates draft  
5. If feedback = REVISE → Student revises  
6. Loop capped at 2 iterations  
7. Quality score extracted  
8. Logs stored  
9. Memory updated  
10. Final response returned  

If approval is not achieved within the iteration cap:

> ⚠️ System safely terminates and delivers the best available draft.

---

## 🏗 Architecture Overview

### Current Architecture


User → Telegram Bot → Orchestrator
↓
Student Agent
↓
Professor Agent
↓
Quality Scorer
↓
Memory (JSON)
↓
Logs (JSON)
↓
Groq LLM API


### Key Design Decisions

- Centralized orchestration
- Bounded reflection loop
- Stateless agent communication
- Lightweight memory persistence
- Structured execution logging
- Deterministic termination

---

## 📊 Execution Metadata Logged

Each run stores:

- Draft round 1
- Feedback round 1
- Draft round 2 (if any)
- Feedback round 2
- Final paper
- Approval status
- Quality score
- Execution time
- Model used

Logs are stored as timestamped JSON files for observability and auditing.

---

## 💾 Memory System

- Stores summaries of last 10 runs
- Keyword-based retrieval
- Context injection into draft generation
- Lightweight, file-based persistence

### Limitation:
Not semantic. Does not use embeddings or vector similarity.

---

## 💰 Cost Optimization Strategy

- Uses `llama-3.1-8b-instant` via Groq API
- Bounded iteration (max 2)
- Controlled token limits
- Lightweight memory truncation
- No paid search APIs

---

## ⚠️ Known Limitations

- No tool usage (no web search)
- No semantic vector memory
- No distributed concurrency
- LLM-based evaluation not benchmarked against human scoring
- Approval detection uses structured keyword parsing (can be improved with strict schema)

---

## 🛠 Future Improvements

- Vector DB memory (FAISS / Pinecone)
- Tool-augmented retrieval (RAG)
- Multi-model evaluation ensemble
- Strict JSON schema output enforcement
- Distributed worker architecture
- Containerized cloud deployment
- API gateway with rate limiting
- Dynamic iteration depth based on quality score

---

## 🏢 Scalability Roadmap

### Current:
- Single-process execution
- File-based storage
- Local deployment

### Production-Ready Architecture:
- Containerized services (Docker)
- Message queue (Redis/Kafka)
- PostgreSQL or managed DB
- Horizontal scaling
- Cloud logging & monitoring
- Multi-model routing

---

## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/aether-agentic-ai.git
cd aether-agentic-ai
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure Environment Variables

Create .env file:

GROQ_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
4️⃣ Run Telegram Bot
python -m bot.student_bot
🧪 Example Usage

Send a topic:

Agentic AI in Healthcare

The system will:

Draft paper

Show professor critique

Revise if needed

Return final version

Display execution summary

📈 Potential Use Cases

Academic research drafting

Enterprise documentation workflows

Legal memo generation

Technical whitepaper generation

Autonomous content QA systems

Structured AI quality validation layers

💡 Monetization Potential

SaaS subscription model

Enterprise AI quality layer

Academic institutional licensing

White-label agentic research API

Domain-specialized agent packages

🏁 Final Note

Aether demonstrates how AI systems can be:

Controlled

Observable

Modular

Bounded

Scalable

Production-aware

It is a step toward structured Agentic AI system design beyond simple generative prompting.
