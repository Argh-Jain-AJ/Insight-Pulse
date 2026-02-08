import sqlite3
import json

def diagnostic():
    conn = sqlite3.connect('insight_pulse.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    tenant = c.execute('SELECT * FROM tenants WHERE id = 1').fetchone()
    print(f"Tenant: {tenant['name']}")
    
    comps = [r['name'] for r in c.execute('SELECT name FROM competitors WHERE tenant_id = 1').fetchall()]
    print(f"Competitors: {comps}")
    
    prods = [r['name'] for r in c.execute('SELECT name FROM products WHERE tenant_id = 1').fetchall()]
    print(f"Products: {prods}")
    
    # Run scoping diagnostic
    import scoping
    tenant_context = {
        "tenant_name": tenant['name'],
        "competitors": comps,
        "products": prods
    }
    
    # Fetch events from DB as list of dicts
    event_rows = c.execute('SELECT source, raw_json FROM events').fetchall()
    events = []
    for r in event_rows:
        try:
            evt = json.loads(r['raw_json'])
            evt['source'] = r['source'] # Ensure source is there
            events.append(evt)
        except: continue
        
    scoped = scoping.filter_signals(events, tenant_context)
    print(f"Scoped Signals (passing filter): {len(scoped)}")
    
    if len(scoped) > 0:
        print("\nSample Scoped Signals:")
        for s in scoped[:5]:
            print(f"- [{s.get('source')}] {s.get('headline', 'N/A')[:50]}")

    conn.close()

if __name__ == "__main__":
    diagnostic()
