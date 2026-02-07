from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import json
import os
from dotenv import load_dotenv

# Load Environment Variables from .env
load_dotenv()

import data_agent1 # For event_ingestion_node
import scoping
import orchestrator
import category_gate
import context_builder
from db import get_db

from pydantic import BaseModel

app = FastAPI(title="Insight Pulse API")

class CompetitorCreate(BaseModel):
    name: str
    tier: Optional[str] = "Tier 1"

class ProductCreate(BaseModel):
    name: str
    therapeutic_area: Optional[str]
    indication: Optional[str]
    phase: Optional[str] = "Marketed"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/process")
def process_pipeline(tenant_id: int = 1):
    db = get_db()
    cursor = db.cursor()
    
    # Fetch Tenant Config (Needed for Scoping & Orchestration & Context)
    tenant = cursor.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
    if not tenant:
        return {"status": "error", "message": "Tenant not found"}
        
    # Fetch Competitors
    comp_rows = cursor.execute("SELECT name FROM competitors WHERE tenant_id = ?", (tenant_id,)).fetchall()
    competitors = [row["name"] for row in comp_rows]
    
    # Fetch Products
    prod_rows = cursor.execute("SELECT name FROM products WHERE tenant_id = ?", (tenant_id,)).fetchall()
    products = [row["name"] for row in prod_rows]
    
    tenant_context = {
        "tenant_name": tenant["name"],
        "competitors": competitors,
        "products": products
    }

    # Phase 12 Step 7: Epistemic Honesty / Reset stale data
    # Clear old insights and context blocks for this run to avoid "staying throughout"
    cursor.execute("DELETE FROM context_blocks WHERE focal_entity_id IN (SELECT id FROM competitors WHERE tenant_id = ?) OR focal_entity_id IN (SELECT id FROM products WHERE tenant_id = ?)", (tenant_id, tenant_id))
    cursor.execute("DELETE FROM insights WHERE tenant_id = ?", (tenant_id,))
    db.commit()

    # 1. Ingestion (Phase 1)
    query = tenant["name"]
    ingestion_output = data_agent1.event_ingestion_node(query, competitors, products)
    events = ingestion_output.get("events", [])
    
    import sys
    sys.stderr.write(f"DEBUG: Ingested {len(events)} events.\n")

    # Store NEW events
    # We need to deduplicate against DB to avoid constraint errors if unique keys exist?
    # Schema says: events(id, source, raw_json, timestamp, processed_flag, tenant_id ...)
    # Let's just try insert and ignore errors or check first.
    # The user's code used a loop with INSERT.
    
    inserted_events = []
    for e in events:
        # Schema: events(id, tenant_id, source, raw_json, timestamp, processed_flag)
        # We skip deduplication on URL for now as column doesn't exist.
        
        cursor.execute("""
            INSERT INTO events (tenant_id, source, raw_json, timestamp, processed_flag)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tenant_id,
            e.get("source"),
            json.dumps(e),
            e.get("collected_at"),
            0
        ))
        inserted_events.append(e)

    db.commit()
    
    # 2. Tenant scoping (Phase 2)
    scoped_signals = scoping.filter_signals(events, tenant_context) 

    # Phase 12 Step 2: Add Cheap Memory
    import memory
    scoped_signals = memory.annotate_signals(scoped_signals)

    # 3. Insight synthesis (Phase 4)
    insights = orchestrator.run_orchestrator(scoped_signals, tenant_context) 

    # Phase 12 Step 3: Subject Validation (Improved for partial matches)
    valid_insights = []
    allowed_entities = tenant_context["competitors"] + tenant_context["products"]
    
    for ins in insights:
        subjects = ins.get("subjects", [])
        validated_subjects = []
        
        for s in subjects:
            # Direct match
            if s in allowed_entities:
                validated_subjects.append(s)
                continue
            
            # Fuzzy/Substring match: e.g. "Abemaciclib (Verzenio)" -> "Verzenio"
            for allowed in allowed_entities:
                if allowed.lower() in s.lower():
                    validated_subjects.append(allowed)
                    break
        
        # Deduplicate
        validated_subjects = list(set(validated_subjects))
        
        if not validated_subjects:
            sys.stderr.write(f"DEBUG: Insight rejected due to NO valid subjects: {ins.get('explanation')[:100]}\n")
            continue
            
        ins["subjects"] = validated_subjects
        valid_insights.append(ins)

    # 4. Category gate (Step 6 REORDERING: Run AFTER suppression and validation)
    final_insights = []
    for ins in valid_insights:
        final_insights.append(category_gate.run_category_gate(ins))

    # 5. Store insights
    insight_ids = []
    for ins in final_insights:
        cursor.execute("""
            INSERT INTO insights
            (tenant_id, scope, severity, velocity, explanation, category, subjects, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            tenant_id,
            ins.get("scope"),
            ins.get("severity"),
            ins.get("velocity"),
            ins.get("explanation"),
            ins.get("category"),
            json.dumps(ins.get("subjects", [])) # Store subjects
        ))
        insight_ids.append(cursor.lastrowid)

    db.commit()

    # 6. Context blocks (Phase 6)
    # Fixed: Pass tenant_id
    context_builder.build_and_store_context_blocks(final_insights, insight_ids, db, tenant_id)

    return {
        "status": "success",
        "insights_generated": len(final_insights)
    }

@app.get("/api/dashboard")
def dashboard():
    db = get_db()
    cursor = db.cursor()

    rows = cursor.execute("""
        SELECT * FROM insights
        WHERE created_at >= datetime('now', '-30 days')
    """).fetchall()

    recent = []
    theme = []
    gtm = []
    positioning = []

    for r in rows:
        ins = dict(r)

        if ins["severity"] == "high" or ins["velocity"] == "increasing":
            recent.append(ins)

        if ins["category"] == "Theme":
            theme.append(ins)
        elif ins["category"] == "GTM":
            gtm.append(ins)
        elif ins["category"] == "Positioning":
            positioning.append(ins)

    return {
        "recent_activity": recent,
        "general_insights": {
            "Theme": theme,
            "GTM": gtm,
            "Positioning": positioning
        },
        "rolling_pulse": rows[:5] # Mock rolling pulse with some recent data
    }

@app.get("/api/competitors")
def list_competitors():
    db = get_db()
    cursor = db.cursor()

    competitors = cursor.execute(
        "SELECT id, name, tier FROM competitors"
    ).fetchall()

    result = []

    for c in competitors:
        # Get counts for high severity specifically for the UI
        high_sev_count = cursor.execute("""
            SELECT COUNT(*) FROM insights i
            JOIN context_blocks cb ON cb.insight_id = i.id
            WHERE cb.focal_entity_type = 'competitor'
            AND cb.focal_entity_id = ?
            AND i.severity = 'high'
        """, (c["id"],)).fetchone()[0]

        total_count = cursor.execute("""
            SELECT COUNT(*) FROM context_blocks
            WHERE focal_entity_type = 'competitor'
            AND focal_entity_id = ?
        """, (c["id"],)).fetchone()[0]

        result.append({
            "id": c["id"],
            "name": c["name"],
            "tier": c["tier"] or "Emerging", 
            "insight_count": total_count,
            "high_severity_count": high_sev_count
        })

    return result

@app.get("/api/competitors/{competitor_id}")
def competitor_detail(competitor_id: int):
    db = get_db()
    cursor = db.cursor()
    
    # Fetch blocks
    blocks = cursor.execute("""
        SELECT * FROM context_blocks
        WHERE focal_entity_type = 'competitor'
        AND focal_entity_id = ?
    """, (competitor_id,)).fetchall()

    grouped = {
        "Theme": [],
        "GTM": [],
        "Positioning": [],
        "Uncategorized": []
    }

    for b in blocks:
        # Fetch insight details
        insight = cursor.execute("""
            SELECT * FROM insights WHERE id = ?
        """, (b["insight_id"],)).fetchone()

        if insight:
            cat = insight["category"]
            if not cat:
                cat = "Uncategorized"
                
            grouped[cat].append({
                "insight": dict(insight),
                "context_framing": b["framing_text"]
            })

    return grouped

@app.get("/api/products")
def list_products():
    db = get_db()
    cursor = db.cursor()

    products = cursor.execute("""
        SELECT id, name, therapeutic_area, indication, phase
        FROM products
    """).fetchall()

    result = []

    for p in products:
        count = cursor.execute("""
            SELECT COUNT(*)
            FROM context_blocks
            WHERE focal_entity_type = 'product'
            AND focal_entity_id = ?
        """, (p["id"],)).fetchone()[0]

        result.append({
            "id": p["id"],
            "name": p["name"],
            "therapeutic_area": p["therapeutic_area"] or "N/A",
            "indication": p["indication"] or "N/A",
            "phase": p["phase"] or "N/A",
            "insight_count": count
        })

    return result

@app.get("/api/products/{product_id}")
def product_detail(product_id: int):
    db = get_db()
    cursor = db.cursor()

    blocks = cursor.execute("""
        SELECT *
        FROM context_blocks
        WHERE focal_entity_type = 'product'
        AND focal_entity_id = ?
    """, (product_id,)).fetchall()

    grouped = {
        "Direct": [],
        "Adjacent": []
    }

    for b in blocks:
        insight = cursor.execute("""
            SELECT *
            FROM insights
            WHERE id = ?
        """, (b["insight_id"],)).fetchone()
        
        if insight:
            # Logic: If scope is 'product' -> Direct. If 'market' or 'competitor' -> Adjacent
            scope = insight["scope"]
            cat = "Direct" if scope == 'product' else "Adjacent"

            grouped[cat].append({
                "insight": dict(insight),
                "context_framing": b["framing_text"]
            })

    return grouped

@app.post("/api/competitors")
def add_competitor(comp: CompetitorCreate, tenant_id: int = 1):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO competitors (tenant_id, name, tier) VALUES (?, ?, ?)",
            (tenant_id, comp.name, comp.tier)
        )
        db.commit()
        return {"status": "success", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/competitors/{comp_id}")
def delete_competitor(comp_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM competitors WHERE id = ?", (comp_id,))
    db.commit()
    return {"status": "success"}

@app.post("/api/products")
def add_product(prod: ProductCreate, tenant_id: int = 1):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (tenant_id, name, therapeutic_area, indication, phase) VALUES (?, ?, ?, ?, ?)",
            (tenant_id, prod.name, prod.therapeutic_area, prod.indication, prod.phase)
        )
        db.commit()
        return {"status": "success", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/products/{prod_id}")
def delete_product(prod_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (prod_id,))
    db.commit()
    return {"status": "success"}
