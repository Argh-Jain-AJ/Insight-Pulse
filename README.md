# Insight Pulse

**Always-on market intelligence for pharmaceutical decision-making.**

Insight Pulse is an agentic system that ingests market signals (news, regulatory updates, competitor moves) and synthesized them into structured, decision-ready insights.

---

## **🚀 Quick Start: Demo Version**

To see the system in action without setting up LLMs or data pipelines, run the **Demo Version**.

This version uses a static snapshot of a real pipeline run, demonstrating:
- **Noise Suppression**: How the system filters out irrelevant news.
- **Silence as Signal**: Why some competitors show no updates.
- **Entity Context**: How the same insight is framed differently for different products.

### **1. Install Backend Dependencies**
```bash
pip install fastapi uvicorn
```

### **2. Run the Demo Backend**
```bash
python demo_main.py
```
*The API server will start on `http://localhost:8000`.*

### **3. Run the Frontend**
Open a new terminal and run:
```bash
cd frontend
npm install
npm run dev
```
*The UI will live at `http://localhost:3000`.*

### **4. Explore the Data**
- **Dashboard**: [http://localhost:3000](http://localhost:3000)
- **API Direct**: [http://localhost:8000/api/dashboard](http://localhost:8000/api/dashboard)

---

## **System Architecture (Full Version)**

The full system (available in `main.py`) consists of:
1.  **Ingestion Agent**: Fetches and normalizes raw events.
2.  **Main Insight Orchestrator**: Synthesizes unexpected changes into candidate insights.
3.  **Lens Agents**: specialized reviewers for Theme, GTM, and Positioning.
4.  **Context Pipeline**: Generates relative framing for detailed tracker views.

*See `RootPrompt.txt` and pipeline specification files for detailed architectural constraints.*
