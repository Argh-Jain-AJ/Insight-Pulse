import orchestrator
from state import AgentState
import json

def verify_phase4_refined():
    print("--- Verifying Phase 4 (Refined) ---")
    
    # 1. Mock Data
    mock_signals = [
        {
            "source": "PharmaNews",
            "headline": "Pfizer cuts pricing for OncologyDrug-X by 15%",
            "description": "Pfizer announced a 15% price reduction.",
            "source_type": "news",
            "company_mentions": ["Pfizer"],
            "drug_mentions": ["OncologyDrug-X"]
        },
        # Add more to potentially trigger limit if LLM is verbose (unlikely with 2 signals)
        {
            "source": "FDA",
            "headline": "New Guidelines for Oncology",
            "description": "FDA releases new draft guidance.",
            "source_type": "regulatory",
            "company_mentions": [],
            "drug_mentions": []
        }
    ]
    
    mock_context = {
        "tenant_name": "Acme Pharma",
        "competitors": ["Pfizer", "Moderna"],
        "products": ["OncologyDrug-X"]
    }
    
    initial_state = AgentState(
        signals=mock_signals,
        tenant_context=mock_context,
        candidate_insights=[],
        errors=[]
    )
    
    # 2. Build & Invoke
    print("Invoking Refined Orchestrator...")
    try:
        app = orchestrator.build_orchestrator_graph()
        final_state = app.invoke(initial_state)
    except Exception as e:
        print(f"❌ Execution Failed: {e}")
        return

    insights = final_state.get("candidate_insights", [])
    errors = final_state.get("errors", [])

    if errors:
        print(f"❌ Errors reported: {errors}")
        
    print(f"Generated {len(insights)} insights.")
    
    # 3. Validation
    if len(insights) > 5:
        print(f"❌ FAILED: Exceeded max limit of 5. Got {len(insights)}.")
        
    for i, ins in enumerate(insights):
        print(f"Insight {i+1}: {ins.get('explanation')[:50]}...")
        if ins.get("category"):
            print(f"❌ FAILED: Insight has category value: {ins['category']}")
        else:
            print("✅ Category is Clean (None/Missing).")
            
    print("--- Phase 4 Refined Verification Complete ---")

if __name__ == "__main__":
    verify_phase4_refined()
