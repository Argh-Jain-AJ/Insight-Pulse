from fastapi.testclient import TestClient
from main import app
import database

client = TestClient(app)

def test_api_process_and_retrieve():
    print("--- Testing Phase 7 API ---")
    
    # 1. Reset DB for clean test
    database.init_db()
    database.seed_db() # Ensures we have Tenant 1, Competitors, Products
    
    # 2. Trigger Pipeline
    print("1. Triggering Pipeline (POST /api/process)...")
    response = client.post("/api/process?tenant_id=1")
    assert response.status_code == 200, f"Pipeline failed: {response.text}"
    data = response.json()
    print(f"✅ Pipeline Success: {data}")
    assert data["insights_generated"] >= 0
    
    # 3. Check Insights
    print("2. Fetching Insights (GET /api/dashboard - simulates querying)...")
    # Using dashboard access as it fetches recent insights
    resp_dash = client.get("/api/dashboard")
    assert resp_dash.status_code == 200
    dash_data = resp_dash.json()
    recent = dash_data.get("recent_activity", [])
    print(f"✅ Dashboard Fetched. Recent Activity: {len(recent)}")
    
    # 4. Check Context via Competitors API
    # We seeded: Competitor 1 (Pfizer)
    print("3. Fetching Context (GET /api/competitors/1)...")
    
    resp_ctx_comp = client.get("/api/competitors/1")
    assert resp_ctx_comp.status_code == 200
    ctx_comp = resp_ctx_comp.json()
    # ctx_comp is grouped by category: {"Theme": [], ...}
    
    total_blocks = sum(len(items) for items in ctx_comp.values())
    print(f"✅ Competitor Context (Pfizer): Found {total_blocks} blocks.")
    
    # Print sample if exists
    for cat, items in ctx_comp.items():
        if items:
            print(f"   Category: {cat}, Sample Framing: {items[0]['framing_text']}")
            assert "Pfizer" in items[0]['framing_text']

    print("--- Phase 7 API Tests Complete ---")

if __name__ == "__main__":
    test_api_process_and_retrieve()
