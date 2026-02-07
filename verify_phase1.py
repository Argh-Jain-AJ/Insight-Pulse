import sqlite3
import os
import database

DB_NAME = "insight_pulse.db"

def verify_phase1():
    print("--- Verifying Phase 1: Database Foundation ---")
    
    # 1. Clean verify (optional, but good for idempotency check)
    # We won't delete the DB to respect persistence, but we expect it to exist after database.py runs.
    
    # Run init and seed
    database.init_db()
    database.seed_db()
    
    if not os.path.exists(DB_NAME):
        print(f"❌ FAILED: Database file {DB_NAME} not found.")
        return

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 2. Verify Tables Exist
    tables = ["tenants", "competitors", "products", "events", "insights", "context_blocks"]
    for t in tables:
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{t}'")
        if not c.fetchone():
            print(f"❌ FAILED: Table '{t}' missing.")
        else:
            print(f"✅ Table '{t}' exists.")
            
    # 3. Verify Seeded Data
    # Tenant
    tenant = c.execute("SELECT * FROM tenants WHERE name='Acme Pharma'").fetchone()
    if tenant:
        print(f"✅ Tenant 'Acme Pharma' found (ID: {tenant['id']}).")
    else:
        print("❌ FAILED: Tenant 'Acme Pharma' missing.")
        
    # Competitors
    comps = c.execute("SELECT * FROM competitors").fetchall()
    comp_names = {r['name'] for r in comps}
    expected_comps = {"Pfizer", "Moderna", "Johnson & Johnson"}
    if expected_comps.issubset(comp_names):
        print(f"✅ Competitors seeded correctly: {comp_names}")
    else:
        print(f"❌ FAILED: Competitors mismatch. Found: {comp_names}")

    # Products
    prods = c.execute("SELECT * FROM products").fetchall()
    prod_names = {r['name'] for r in prods}
    expected_prods = {"OncologyDrug-X", "CardioDrug-Y"}
    if expected_prods.issubset(prod_names):
        print(f"✅ Products seeded correctly: {prod_names}")
    else:
        print(f"❌ FAILED: Products mismatch. Found: {prod_names}")

    # 4. Verify Insight Category Nullable
    # Attempt to insert an insight with NULL category
    try:
        c.execute('''
            INSERT INTO insights (tenant_id, scope, severity, velocity, explanation, category, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tenant['id'], "market", "high", "fast", "Test Insight", None, "2023-01-01"))
        print("✅ Insight with NULL category inserted successfully (Invariant held).")
    except sqlite3.IntegrityError as e:
        print(f"❌ FAILED: Could not insert insight with NULL category. Error: {e}")

    # 5. Verify Event Storage
    test_events = [
        {
            "source": "Test Source",
            "raw_json": {"foo": "bar"},
            "collected_at": "2023-10-27T10:00:00"
        }
    ]
    
    # We need to close our local connection to let the module use its own connection logic if it wasn't sharing
    # (sqlite is file based so it's fine, but good practice)
    conn.commit()
    conn.close()
    
    # Call functionality
    new_ids = database.store_events(test_events)
    
    # Verify
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if len(new_ids) == 1:
        evt = c.execute("SELECT * FROM events WHERE id=?", (new_ids[0],)).fetchone()
        if evt:
            print(f"✅ Event stored. ID: {evt['id']}, Processed: {evt['processed_flag']}")
            if evt['raw_json'] == '{"foo": "bar"}':
                 print("✅ Raw JSON preserved.")
            else:
                 print(f"❌ FAILED: Raw JSON mismatch. Got: {evt['raw_json']}")
        else:
            print("❌ FAILED: Event not found after storage.")
    else:
         print(f"❌ FAILED: store_events returned {len(new_ids)} IDs, expected 1.")

    conn.close()
    print("--- Phase 1 Verification Complete ---")

if __name__ == "__main__":
    verify_phase1()
