# Insight Pulse 

**Always-on market intelligence for pharmaceutical decision-making.**

Insight Pulse is an **agentic AI pipeline** that monitors competitor moves, clinical updates, and regulatory shifts. It transforms fragmented market signals into structured, high-fidelity strategic insights categorized by **Theme, GTM, and Positioning**.

###  [**Watch the Demo Video**](https://plakshauniversity1-my.sharepoint.com/:v:/g/personal/vibhav_sahu_ug24_plaksha_edu_in/IQA_dYT81YFwSaHV-OKDyZgvAYUpb2FtFH7Pg6RTFqycWpg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=600O2l)

---

##  Choose Your Mode

Depending on your environment, you can run Insight Pulse in two ways:

### 1.  Quick Start: Seamless Demo Mode
*Run the system in seconds without LLMs, API keys, or specialized hardware.*

The dashboard is built with a **Seamless Demo Mode** that uses precomputed high-fidelity data to showcase noise suppression, strategic mapping, and longitudinal tracking.

1. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. **Access Dashboard**: Open [http://localhost:3000](http://localhost:3000).
3. **Trigger Demo**: Click ** Run Pipeline**. When prompted that the backend is unavailable, click **OK** to enable Demo Mode.

---

###  2. Full Implementation: Real-World Pipeline
*Run the live agentic pipeline for real-time market intelligence.*

#### **Requirements**
- **Python 3.10+**
- **Ollama** (running locally with `qwen2.5:3b` model)
- **API Keys**: NewsAPI key added to a root `.env` file.

#### **Setup & Run**
1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn requests langchain langchain_community python-dotenv
   cd frontend && npm install
   ```
2. **Configure Environment**: Create a `.env` in the root:
   ```env
   NEWSAPI_KEY=your_key_here
   ```
3. **Start Backend**:
   ```bash
   uvicorn main:app --reload
   ```
4. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
5. **Generate Insights**: Click ** Run Pipeline** in the dashboard. The system will ingest live signals and synthesize new strategic insights into the database.

---

##  Architecture & Documentation

Insight Pulse follows a modular **6-stage pipeline**:
1. **Ingestion**: Multi-source gathering from NewsAPI, FDA, and USPTO.
2. **Scoping**: Tenant-specific relevance filtering.
3. **Memory**: MD5 fingerprinting for deduplication and velocity tracking.
4. **Synthesis**: LLM orchestration (Few-Shot Prompting).
5. **Categorization**: Multi-lens auditing for Theme, GTM, and Positioning.
6. **Framing**: Strategic context linkage for focal entities.

For a deep dive into the code and data flow, see [docs/system_architecture.md](docs/system_architecture.md).

##  Tech Stack
- **Frontend**: Next.js 14, Tailwind CSS, Lucide React.
- **Backend**: FastAPI (Python 3.10).
- **Intelligence**: LangGraph, Ollama (Qwen 2.5 3B).
- **Storage**: SQLite (insight_pulse.db).
