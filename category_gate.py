from typing import Dict, Optional
import lenses

def run_category_gate(insight: Dict) -> Dict:
    """
    Single entry point for categorization.
    1. Runs all lenses (Theme, GTM, Positioning).
    2. Calls assign_category with scores.
    3. Returns updated insight.
    """
    # 1. Run Lenses
    theme_score = lenses.run_theme_lens(insight)
    gtm_score = lenses.run_gtm_lens(insight)
    pos_score = lenses.run_positioning_lens(insight)
    
    # 2. Assign Category
    return assign_category(insight, theme_score, gtm_score, pos_score)


def assign_category(
    insight: Dict, 
    theme_conf: float, 
    gtm_conf: float, 
    pos_conf: float
) -> Dict:
    """
    Phase 5: Category Gate Logic.
    
    Authoritative assignment of category based on lens confidence scores.
    
    Rules:
    - Threshold: >= 0.5
    - Winner: Max score wins
    - If max < 0.5: Category remains None
    - NO other modifications allowed.
    """
    
    # Copy to avoid mutating original if needed, though usually we modify state in place in LangGraph
    # We'll work on a copy to be safe given the "Do not alter" instruction for lenses, 
    # but here we ARE the gate, so we modify.
    updated_insight = insight.copy()
    
    # 1. Identify valid candidates
    scores = {
        "Theme": theme_conf,
        "GTM": gtm_conf,
        "Positioning": pos_conf
    }
    
    # 2. Find Max
    best_category = max(scores, key=scores.get)
    max_score = scores[best_category]
    
    # 3. Apply Threshold
    if max_score >= 0.5:
        updated_insight["category"] = best_category
    else:
        # Explicitly ensure it is None (or preserve existing None)
        # Note: If it already had a category (which it shouldn't from Orchestrator), 
        # this logic would overwrite it based on current scores. 
        # Implementation Step 17 says: "If max < 0.5: leaves insight.category as None".
        # Safe to force None if we want to be strict, or just pass. 
        # Given "Category appears ONLY after the gate", we assume input is None.
        updated_insight["category"] = None
        
    return updated_insight
