import json
from typing import Dict, Optional
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# -----------------------------------------------------------------------------
# PROMPT DEFINITIONS
# -----------------------------------------------------------------------------

THEME_PROMPT = """
You are the **Theme Lens Agent** for Insight Pulse.
Your job is to evaluate if an insight represents a broad **THEME** or **SECTOR-WIDE** pattern.

**DEFINITION**:
A "Theme" insight involves:
- Market-wide shifts (e.g., regulatory changes, new standards).
- Sector trends affecting multiple players.
- Structural changes in the industry environment.

**INPUT INSIGHT**:
Explanation: {explanation}
Scope: {scope}
Severity: {severity}

**TASK**:
Rate your confidence that this insight is primarily a "Theme".
Return a JSON object with a single field: "confidence" (float between 0.0 and 1.0).

**EXAMPLES**:
- FDA new guidelines -> 0.95
- Competitor Price Cut -> 0.1 (This is GTM, not Theme)
- New CEO -> 0.2

Return JSON ONLY.
"""

GTM_PROMPT = """
You are the **GTM Lens Agent** for Insight Pulse.
Your job is to evaluate if an insight represents a **GO-TO-MARKET (GTM)** move.

**DEFINITION**:
A "GTM" insight involves:
- Pricing and contracting changes.
- Sales models and channel strategies.
- Market access, reimbursement, or distribution.
- Commercial execution.

**INPUT INSIGHT**:
Explanation: {explanation}
Scope: {scope}
Severity: {severity}

**TASK**:
Rate your confidence that this insight is primarily "GTM".
Return a JSON object with a single field: "confidence" (float between 0.0 and 1.0).

**EXAMPLES**:
- Price reduction -> 0.95
- New sales team structure -> 0.9
- FDA guidelines -> 0.1 (This is Theme)

Return JSON ONLY.
"""

POSITIONING_PROMPT = """
You are the **Positioning Lens Agent** for Insight Pulse.
Your job is to evaluate if an insight represents a **POSITIONING** or **MESSAGING** shift.

**DEFINITION**:
A "Positioning" insight involves:
- Brand messaging and differentiation.
- Target segment redefinition.
- Value proposition changes.
- Marketing claims or label updates (commercial focus).

**INPUT INSIGHT**:
Explanation: {explanation}
Scope: {scope}
Severity: {severity}

**TASK**:
Rate your confidence that this insight is primarily "Positioning".
Return a JSON object with a single field: "confidence" (float between 0.0 and 1.0).

**EXAMPLES**:
- "Our drug is now 1st line" -> 0.95
- Rebranding campaign -> 0.9
- Price cut -> 0.1 (This is GTM)

Return JSON ONLY.
"""

# -----------------------------------------------------------------------------
# LENS IMPLEMENTATION
# -----------------------------------------------------------------------------

class LensAgent:
    def __init__(self, prompt_template: str, name: str):
        self.llm = Ollama(
            model="qwen2.5:3b",
            temperature=0.1,
            timeout=30,
            format="json"
        )
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.name = name

    def run(self, insight: Dict) -> float:
        """
        Runs the lens on an insight and returns a confidence score (0.0 - 1.0).
        Returns 0.0 on any error.
        """
        try:
            # Format Prompt
            formatted = self.prompt.format(
                explanation=insight.get("explanation", ""),
                scope=insight.get("scope", ""),
                severity=insight.get("severity", "")
            )
            
            # Invoke LLM
            response = self.llm.invoke(formatted)
            
            # Parse JSON
            data = self._parse_json(response)
            
            # Extract Confidence
            confidence = float(data.get("confidence", 0.0))
            
            # Clamp constraints
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            # Fail safe: return 0.0
            return 0.0

    def _parse_json(self, text: str) -> Dict:
        import json
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.endswith("```"):
            clean = clean[:-3]
        try:
            return json.loads(clean)
        except:
            return {}

# Instantiate Agents
theme_lens_agent = LensAgent(THEME_PROMPT, "Theme")
gtm_lens_agent = LensAgent(GTM_PROMPT, "GTM")
positioning_lens_agent = LensAgent(POSITIONING_PROMPT, "Positioning")

# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------

def run_theme_lens(insight: Dict) -> float:
    return theme_lens_agent.run(insight)

def run_gtm_lens(insight: Dict) -> float:
    return gtm_lens_agent.run(insight)

def run_positioning_lens(insight: Dict) -> float:
    return positioning_lens_agent.run(insight)
