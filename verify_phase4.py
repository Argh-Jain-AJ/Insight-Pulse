import orchestrator
from state import AgentState
import json

def verify_phase4():
    print("--- Verifying Phase 4: Main Insight Orchestrator ---")
    
    # 1. Mock Data
    print("1. Preparing Mock State...")
    mock_signals = [
        {
            "source": "PharmaNews",
            "headline": "Pfizer cuts pricing for OncologyDrug-X by 15%",
            "description": "In a surprise move, Pfizer announced a 15% price reduction for its flagship oncology drug effective next month.",
            "source_type": "news",
            "company_mentions": ["Pfizer"],
            "drug_mentions": ["OncologyDrug-X"]
        },
        {
            "source": "MarketWatch",
            "headline": "Competitors react to Pfizer's aggressive pricing strategy",
            "description": "Analysts suggest this pricing war could impact margins across the sector.",
            "source_type": "news",
            "company_mentions": ["Pfizer"],
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
    
    # 2. Build Graph
    print("2. Building Graph...")
    try:
        app = orchestrator.build_orchestrator_graph()
        print("✅ Graph compiled successfully.")
    except Exception as e:
        print(f"❌ FAILED: Graph compilation failed. {e}")
        return

    # 3. Invoke Graph
    print("3. Invoking Orchestrator (calling Ollama)...")
    try:
        final_state = app.invoke(initial_state)
    except Exception as e:
        print(f"❌ FAILED: Graph execution failed. {e}")
        return
        
    # 4. Analyze Results
    insights = final_state.get("candidate_insights", [])
    errors = final_state.get("errors", [])
    
    if errors:
        print(f"❌ FAILED: Errors detected in state: {errors}")
        
    if not insights:
        print("⚠️ WARNING: No insights generated. This might be due to LLM parsing or prompt issues.")
        # Check raw output if possible (orchestrator doesn't return raw in state, but errors might help)
    else:
        print(f"✅ Generated {len(insights)} insights.")
        print(json.dumps(insights, indent=2))
        
        # 5. Validate Output Structure
        print("4. Validating Structure & Invariants...")
        all_ok = True
        for ins in insights:
            # Check mandatory fields
            required = ["scope", "severity", "velocity", "explanation"]
            if not all(k in ins for k in required):
                print(f"❌ Insight missing required fields: {ins}")
                all_ok = False
            
            # Check Negative Constraint: Category MUST be None
            if ins.get("category") is not None:
                print(f"❌ CRITICAL FAILURE: Insight assigned a category: {ins['category']}")
                all_ok = False
            else:
                print("✅ Invariant Checked: Category is None.")
                
        if all_ok:
            print("✅ SUCCESS: All insights strictly follow schema and constraints.")
            
    print("--- Phase 4 Verification Complete ---")

if __name__ == "__main__":
    verify_phase4()
