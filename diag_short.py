import sqlite3
import json
import scoping

conn = sqlite3.connect('insight_pulse.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

tenant = c.execute('SELECT * FROM tenants WHERE id = 1').fetchone()
comps = [r['name'] for r in c.execute('SELECT name FROM competitors WHERE tenant_id = 1').fetchall()]
prods = [r['name'] for r in c.execute('SELECT name FROM products WHERE tenant_id = 1').fetchall()]

# Limit to latest 133 events to mimic user's run
event_rows = c.execute('SELECT source, raw_json FROM events ORDER BY id DESC LIMIT 133').fetchall()
events = [json.loads(r['raw_json']) for r in event_rows]
for i, r in enumerate(event_rows):
    events[i]['source'] = r['source']

tenant_context = {"tenant_name": tenant['name'], "competitors": comps, "products": prods}
scoped = scoping.filter_signals(events, tenant_context)

print(f"LATEST_RUN_RAW: {len(events)}")
print(f"LATEST_RUN_SCOPED: {len(scoped)}")
if scoped:
    print("\nTOP 5 SCOPED HEADLINES:")
    for s in scoped[:5]:
        print(f"- {s.get('headline')[:100]}")
conn.close()
