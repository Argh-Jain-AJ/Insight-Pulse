import json
from typing import List, Dict, Any, Optional
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

from state import AgentState

# -----------------------------------------------------------------------------
# PROMPT DESIGN
# -----------------------------------------------------------------------------
ORCHESTRATOR_PROMPT_TEMPLATE = """
You are the **Main Insight Orchestrator** for the Insight Pulse system.
Your job is to synthesize a list of structured Insights from raw market signals.

**TENANT CONTEXT**:
- Name: {tenant_name}
- Tracked Competitors: {competitors}
- Tracked Products: {products}

**INPUT SIGNALS**:
{signals_text}

**STRICT RULES**:
1. **SUPPRESSION**: Most inputs produce ZERO insights. Do NOT create an insight unless there is clear change, recurrence, or escalation. Single isolated signals MUST be suppressed.
2. **SEVERITY**: high (multi-subject/repeat), medium (one subject/emerging), low (isolated).
3. **VELOCITY**: increasing (repeat), stable (single), decreasing (absent).
4. **SUBJECTS**: list of names (verbatim from context) affected by the insight.
5. **JSON ONLY**: Return ONLY a valid JSON array of objects.

**OUTPUT SCHEMA**:
[
  {{
    "scope": "competitor | product | market",
    "subjects": ["Name1", "Name2"],
    "severity": "low | medium | high",
    "velocity": "decreasing | stable | increasing",
    "explanation": "concise string"
  }}
]

Return STRICT JSON only.
"""

RETRY_PROMPT = "Return valid JSON only. Do not include any other text."

class OrchestratorNode:
    def __init__(self):
        self.llm = Ollama(
            model="qwen2.5:3b",
            temperature=0.1,
            timeout=60,
            format="json"
        )
        self.prompt = PromptTemplate.from_template(ORCHESTRATOR_PROMPT_TEMPLATE)

    def format_signals(self, signals: List[Dict]) -> str:
        """Formats signals into plain-language bullet points."""
        if not signals:
            return "No signals."
        
        formatted = ""
        for sig in signals:
            source_str = f"[{sig.get('source', 'Unknown')}]"
            headline = sig.get("headline", "N/A")
            desc = sig.get("description", "")
            
            # Step 2: Memory Annotation
            status = " (REPEAT SIGNAL)" if sig.get("_seen_before") else " (NEW SIGNAL)"
            
            formatted += f"- {source_str} {headline}: {desc}{status}\n"
        return formatted

    def is_insight_strong(self, insight: Dict) -> bool:
        """Guardrail to reject weak/speculative insights."""
        explanation = insight.get("explanation", "").lower()
        # Only reject if it's explicitly speculative hearsay
        weak_markers = [
            "one report", "single signal", "unconfirmed", 
            "speculated", "rumored", "may be a result of"
        ]
        return not any(w in explanation for w in weak_markers)

    def validate_insight(self, insight: Dict) -> bool:
        """
        Validates a single insight object.
        """
        required_fields = ["scope", "severity", "velocity", "explanation", "subjects"]
        
        # 1. Check required fields
        if not all(field in insight for field in required_fields):
            return False
            
        # 2. Check Category Invariant
        if "category" in insight: 
            return False
            
        return True

    def run(self, state: AgentState) -> AgentState:
        tenant = state["tenant_context"]
        signals = state["signals"]

        if not signals:
            return {
                "candidate_insights": [], 
                "errors": state.get("errors", []) + ["No signals provided"]
            }

        # 1. Format Inputs
        signals_text = self.format_signals(signals)
        final_prompt = self.prompt.format(
            tenant_name=tenant.get("tenant_name", "Unknown"),
            competitors=", ".join(tenant.get("competitors", [])),
            products=", ".join(tenant.get("products", [])),
            signals_text=signals_text
        )

        # 2. Invoke LLM (Attempt 1)
        raw_response = ""
        try:
            raw_response = self.llm.invoke(final_prompt)
            import sys
            sys.stderr.write(f"DEBUG: Raw LLM Response: {raw_response[:500]}...\n")
            insights_data = self._parse_json(raw_response)
        except Exception as e:
            import sys
            sys.stderr.write(f"DEBUG: Attempt 1 failed: {e}\n")
            # 3. Retry Logic (Attempt 2)
            try:
                retry_input = f"{final_prompt}\n\nSYSTEM: Previous response was malformed. {RETRY_PROMPT}"
                raw_response = self.llm.invoke(retry_input)
                sys.stderr.write(f"DEBUG: Retry LLM Response: {raw_response[:500]}...\n")
                insights_data = self._parse_json(raw_response)
            except Exception as e:
                # 4. Final Failure
                return {
                   "candidate_insights": [],
                   "errors": state.get("errors", []) + [f"JSON parsing failed after retry. Last error: {str(e)}"]
                }

        # 5. Filter & Limit
        valid_insights = []
        for item in insights_data:
            if self.validate_insight(item) and self.is_insight_strong(item):
                valid_insights.append(item)
            else:
                import sys
                sys.stderr.write(f"DEBUG: Rejected item: {item}\n")
        
        # Step 5: Severity Recalibration (Breadth)
        for ins in valid_insights:
            if ins["severity"] == "high" and len(ins.get("subjects", [])) <= 1:
                # High severity requires either multiple subjects OR (addressed by orchestrator) repeated signals.
                # Here we enforce breadth as a secondary check if breadh is low.
                # Actually, the user says "Single-subject insights never become high".
                ins["severity"] = "medium"

        # Enforce Max 5
        valid_insights = valid_insights[:5]

        # 6. Update State
        return {
            "candidate_insights": valid_insights,
            "errors": state.get("errors", [])
        }

    def _parse_json(self, text: str) -> List[Dict]:
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.endswith("```"):
            clean = clean[:-3]
        data = json.loads(clean)
        
        # Handle wrapped list
        if isinstance(data, dict):
            # If the dict has a key "insights" or "candidate_insights" which is a list, use that
            for key in ["insights", "candidate_insights", "data", "response", "objects"]:
                if key in data and isinstance(data[key], list):
                    return data[key]
            # Otherwise treat the dict itself as a single item
            return [data]
        
        return data

# Wrapper for LangGraph
orchestrator_node = OrchestratorNode()

def synthesize_insights(state: AgentState) -> AgentState:
    return orchestrator_node.run(state)

def build_orchestrator_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("synthesize_insights", synthesize_insights)
    workflow.set_entry_point("synthesize_insights")
    workflow.add_edge("synthesize_insights", END)
    return workflow.compile()

def run_orchestrator(signals: List[Dict], tenant_context: Optional[Dict] = None) -> List[Dict]:
    """
    Wrapper for API usage.
    """
    if tenant_context is None:
        tenant_context = {}
        
    state = {
        "signals": signals,
        "tenant_context": tenant_context,
        "candidate_insights": [],
        "errors": []
    }
    result = synthesize_insights(state)
    return result.get("candidate_insights", [])
