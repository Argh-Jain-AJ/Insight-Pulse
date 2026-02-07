import sqlite3
import json
from datetime import datetime

DB_NAME = "insight_pulse.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Step 1: Create SQLite Database Schema
    """
    conn = get_db_connection()
    c = conn.cursor()

    # 1. tenants
    c.execute('''
        CREATE TABLE IF NOT EXISTS tenants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # 2. competitors
    c.execute('''
        CREATE TABLE IF NOT EXISTS competitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            tier TEXT, -- New: Tier 1, Tier 2, Emerging
            FOREIGN KEY (tenant_id) REFERENCES tenants (id),
            UNIQUE(tenant_id, name)
        )
    ''')

    # 3. products
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            therapeutic_area TEXT, -- New: Oncology, etc.
            indication TEXT,       -- New: NSCLC, etc.
            phase TEXT,            -- New: Phase III, Marketed
            FOREIGN KEY (tenant_id) REFERENCES tenants (id),
            UNIQUE(tenant_id, name)
        )
    ''')

    # 4. events
    # raw_json stored as TEXT
    # processed_flag stored as INTEGER (0/1) for boolean
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER, 
            source TEXT,
            raw_json TEXT,
            timestamp TEXT,
            processed_flag INTEGER DEFAULT 0,
            FOREIGN KEY (tenant_id) REFERENCES tenants (id)
        )
    ''')
    # Note on tenant_id in events: implementation steps don't strictly require it for ingestion 
    # (Step 3 says "Create function that stores it... marks processed_flag False"). 
    # But schema in Step 1 includes tenant_id. 
    # We will allow it to be NULL initially if events are global, or set it if known.
    # For Phase 1 tracebility, we just follow the schema.

    # 5. insights
    # Category MUST be nullable (Critical Invariant)
    c.execute('''
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER NOT NULL,
            scope TEXT NOT NULL,
            severity TEXT NOT NULL,
            velocity TEXT NOT NULL,
            explanation TEXT NOT NULL,
            category TEXT, 
            subjects TEXT, -- JSON list of strings (Phase 12 Step 3)
            created_at TEXT,
            FOREIGN KEY (tenant_id) REFERENCES tenants (id)
        )
    ''')

    # 6. context_blocks
    c.execute('''
        CREATE TABLE IF NOT EXISTS context_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight_id INTEGER NOT NULL,
            focal_entity_id INTEGER NOT NULL,
            focal_entity_type TEXT NOT NULL,
            framing_text TEXT NOT NULL,
            FOREIGN KEY (insight_id) REFERENCES insights (id)
        )
    ''')

    conn.commit()
    conn.close()

    # 7. fingerprints (Phase 12: Memory)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS fingerprints (
            hash TEXT PRIMARY KEY,
            last_seen TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
    print("Database initialized.")

def seed_db():
    """
    Step 2: Seed Initial Data
    """
    conn = get_db_connection()
    c = conn.cursor()

    # 1 tenant: "Eli Lilly"
    try:
        c.execute('INSERT INTO tenants (name) VALUES (?)', ("Eli Lilly",))
        tenant_id = c.lastrowid
    except sqlite3.IntegrityError:
        # Already exists, fetch it
        tenant = c.execute('SELECT id FROM tenants WHERE name = ?', ("Eli Lilly",)).fetchone()
        tenant_id = tenant['id']

    # 5 competitors
    competitors = [
        ("Novo Nordisk", "Tier 1"),
        ("Pfizer", "Tier 1"),
        ("Novartis", "Tier 1"),
        ("Roche", "Tier 1"),
        ("AstraZeneca", "Tier 1")
    ]
    for name, tier in competitors:
        try:
            c.execute('INSERT INTO competitors (tenant_id, name, tier) VALUES (?, ?, ?)', (tenant_id, name, tier))
        except sqlite3.IntegrityError:
            pass 

    # 5 products
    products = [
        ("Mounjaro", "Metabolic", "Type 2 Diabetes", "Marketed"),
        ("Zepbound", "Metabolic", "Obesity", "Marketed"),
        ("Verzenio", "Oncology", "Breast Cancer", "Marketed"),
        ("Taltz", "Immunology", "Psoriasis", "Marketed"),
        ("Jardiance", "Metabolic", "Diabetes/Heart Failure", "Marketed")
    ]
    for name, ta, ind, phase in products:
        try:
            c.execute('INSERT INTO products (tenant_id, name, therapeutic_area, indication, phase) VALUES (?, ?, ?, ?, ?)', 
                      (tenant_id, name, ta, ind, phase))
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    conn.close()
    print("Database seeded.")

def store_events(events_data):
    """
    Step 3: Write Event Storage Function
    Takes list of dicts (from data_agent), stores them.
    Returns list of new event IDs.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    new_ids = []
    
    # In Phase 1, we might not have tenant_id logic strictly defined for *incoming* events 
    # if they are raw global news. Implementation Step 3 doesn't mention assigning tenant_id 
    # at ingestion, but Step 1 schema has it.
    # Logic: Events are often global. We'll leave tenant_id NULL for now or assign to default if needed.
    # However, Step 1 schema has: events - id, tenant_id, ...
    # Let's assume for MVP scope (Acme Pharma is only tenant), we might link them, 
    # OR we treat raw events as raw and link them later? 
    # Re-reading Step 3: "Extract original API response data... Store as raw Event... Mark processed_flag as False"
    # It doesn't explicitly say "assign tenant_id". 
    # But later, "Phase 2: Tenant Scoping Filter" filters signals.
    # So raw events are likely global. We will insert with NULL tenant_id effectively, 
    # unless 'tenant_id' in schema implies strict ownership. 
    # SQLite allows NULL unless NOT NULL is specified. Schema in `init_db` above has `tenant_id INTEGER` (nullable).
    # We will proceed with NULL tenant_id for raw ingestion.
    
    for event in events_data:
        # Extract fields
        source = event.get("source", "Unknown")
        raw_json_str = json.dumps(event.get("raw_json", {}))
        # Use collected_at as timestamp if available, else current time
        timestamp = event.get("collected_at", datetime.utcnow().isoformat())
        
        c.execute('''
            INSERT INTO events (source, raw_json, timestamp, processed_flag)
            VALUES (?, ?, ?, ?)
        ''', (source, raw_json_str, timestamp, 0))
        
        new_ids.append(c.lastrowid)
        
    conn.commit()
    conn.close()
    return new_ids

if __name__ == "__main__":
    # If run directly, initialize and seed
    init_db()
    seed_db()
