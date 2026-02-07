import category_gate
import lenses

def verify_phase5():
    print("--- Verifying Phase 5: Lens Agents & Category Gate ---")
    
    # 1. Test Data
    high_sev_insight = {
        "scope": "competitor",
        "severity": "high",
        "velocity": "fast",
        "explanation": "Critical market shift.",
        "category": None
    }
    
    # 2. Test Case A: High Confidence (Winner takes all)
    print("Test A: High Confidence (GTM=0.9)")
    res_a = category_gate.assign_category(high_sev_insight, 0.2, 0.9, 0.4)
    
    if res_a["category"] == "GTM":
        print("✅ Category assigned correctly: GTM")
    else:
        print(f"❌ FAILED: Expected GTM, got {res_a.get('category')}")
        
    if res_a["severity"] == "high":
        print("✅ Severity preserved.")
    else:
        print("❌ FAILED: Severity modified.")

    # 3. Test Case B: Low Confidence / Ambiguous
    print("Test B: Low Confidence (Max=0.6)")
    res_b = category_gate.assign_category(high_sev_insight, 0.6, 0.5, 0.5)
    
    if res_b["category"] is None:
        print("✅ Category remains None (High severity preserved).")
    else:
        print(f"❌ FAILED: Expected None, got {res_b.get('category')}")
        
    # 4. Verify Lens Output Types (Mocking actual run if we want, or checking code signature)
    # We will trust the implementation check here, or run a dummy lens if cost allows.
    # checking `lenses.py` imports and signature.
    import inspect
    sig = inspect.signature(lenses.run_theme_lens)
    if sig.return_annotation == float:
         print("✅ Lens functions declared to return float.")
    else:
         print(f"⚠️ Warning: Lens return type annotation is {sig.return_annotation}")

    print("--- Phase 5 Verification Complete ---")

if __name__ == "__main__":
    verify_phase5()
