from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """
    Global State Schema for Insight Pulse.
    
    Fields:
    - signals (List[Dict]): Read-only list of relevant signals.
    - tenant_context (Dict): Read-only tenant configuration (name, competitors, products).
    - candidate_insights (List[Dict]): Mutable list of generated insights (uncategorized).
    - errors (List[str]): List of error messages or debugging info.
    """
    signals: List[Dict[str, Any]]
    tenant_context: Dict[str, Any]
    candidate_insights: List[Dict[str, Any]]
    errors: List[str]
