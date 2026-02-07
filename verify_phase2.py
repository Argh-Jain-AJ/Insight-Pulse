import scoping
import json

def verify_phase2():
    print("--- Verifying Phase 2: Tenant Scoping Filter ---")
    
    # Mock Tenant Config
    tenant_config = {
        "name": "Acme Pharma",
        "competitors": ["Pfizer", "Moderna"],
        "products": ["DrugX"]
    }
    
    # Test Data
    test_signals = [
        # Case 1: Competitor Match (Pfizer) -> KEEP
        {
            "id": 1,
            "source_type": "news",
            "company_mentions": ["Pfizer"],
            "drug_mentions": []
        },
        # Case 2: Product Match (DrugX) -> KEEP
        {
            "id": 2,
            "source_type": "news",
            "company_mentions": [],
            "drug_mentions": ["DrugX"]
        },
        # Case 3: Regulatory (FDA) -> KEEP (even without mentions)
        {
            "id": 3,
            "source_type": "regulatory",
            "company_mentions": [],
            "drug_mentions": []
        },
        # Case 4: Irrelevant Competitor -> DISCARD
        {
            "id": 4,
            "source_type": "news",
            "company_mentions": ["UnknownCorp"],
            "drug_mentions": []
        },
        # Case 5: Irrelevant Product -> DISCARD
        {
            "id": 5,
            "source_type": "journal",
            "company_mentions": [],
            "drug_mentions": ["UnknownDrug"]
        },
        # Case 6: Mixed Case Match (pfizer) -> KEEP
        {
            "id": 6,
            "source_type": "news",
            "company_mentions": ["pfizer"], # lowercase
            "drug_mentions": []
        }
    ]
    
    # Execute Filter
    filtered = scoping.filter_signals(test_signals, tenant_config)
    
    # Verification
    kept_ids = {s["id"] for s in filtered}
    expected_ids = {1, 2, 3, 6}
    
    print(f"Input Signals: {len(test_signals)}")
    print(f"Filtered Signals: {len(filtered)}")
    print(f"Kept IDs: {kept_ids}")
    
    if kept_ids == expected_ids:
        print("✅ SUCCESS: Filter logic correctly isolated relevant signals.")
        print("   - Competitor match: OK")
        print("   - Product match: OK")
        print("   - Regulatory safety net: OK")
        print("   - Case-insensitivity: OK")
        print("   - Irrelevant discarded: OK")
    else:
        print(f"❌ FAILED: Expected {expected_ids}, got {kept_ids}")
        missing = expected_ids - kept_ids
        unexpected = kept_ids - expected_ids
        if missing: print(f"   Missing IDs: {missing}")
        if unexpected: print(f"   Unexpected IDs: {unexpected}")
        
    print("--- Phase 2 Verification Complete ---")

if __name__ == "__main__":
    verify_phase2()
