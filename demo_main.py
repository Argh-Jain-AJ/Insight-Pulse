import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any

app = FastAPI(title="Insight Pulse Demo API")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Demo Data
DATA_FILE = "demo_data.json"
if not os.path.exists(DATA_FILE):
    raise RuntimeError(f"Demo data file {DATA_FILE} not found!")

with open(DATA_FILE, "r") as f:
    DEMO_DATA = json.load(f)

# Helper functions
def get_entity_id_by_name(name: str, entity_type: str) -> Optional[int]:
    entities = DEMO_DATA["entities"].get(f"{entity_type}s", []) # products or competitors
    for e in entities:
        if e["name"] == name:
            return e["id"]
    return None

def get_context_blocks_for_entity(entity_id: int, entity_type: str, entity_name: str):
    """
    Filters context blocks for a specific entity.
    """
    blocks = []
    
    # Filter blocks from demo data
    for block in DEMO_DATA["context_blocks"]:
        match_id = False
        
        # We match by name in demo_data for readability, but API uses ID.
        # So we need to reconcile. Let's look up the name for the requested ID.
        target_name = None
        entities = DEMO_DATA["entities"].get(f"{entity_type}s", [])
        for e in entities:
            if e["id"] == entity_id:
                target_name = e["name"]
                break
        
        if not target_name:
            continue

        if block["focal_entity_name"] == target_name and block["focal_entity_type"] == entity_type:
             # Find linked insight
             insight = next((i for i in DEMO_DATA["insights"] if i["id"] == block["insight_id"]), None)
             if insight:
                 blocks.append({
                     "insight": insight,
                     "context_framing": block["framing_text"]
                 })
    return blocks

@app.get("/health")
def health():
    return {"status": "ok", "mode": "demo"}

@app.post("/api/process")
def process_pipeline():
    """
    Mock pipeline trigger. In demo mode, this just says 'Success' 
    as the data is static precomputed.
    """
    return {
        "status": "success",
        "insights_generated": len(DEMO_DATA["insights"]),
        "message": "Demo pipeline 'execution' complete. Static data loaded."
    }

@app.get("/api/dashboard")
def dashboard():
    """
    Returns grouped insights for the dashboard.
    """
    recent = []
    theme = []
    gtm = []
    positioning = []
    
    insights = DEMO_DATA["insights"]
    
    for ins in insights:
        # Recent Market Activity Logic
        if ins["severity"] == "high" or ins["velocity"] in ["increasing", "explosive"]:
            recent.append(ins)
            
        # Category Logic
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
        "rolling_pulse": insights[:5] # Just show all for rolling in demo
    }

@app.get("/api/competitors")
def list_competitors():
    competitors = DEMO_DATA["entities"]["competitors"]
    result = []
    
    for c in competitors:
        # Calculate counts on flight per entity
        blocks = get_context_blocks_for_entity(c["id"], "competitor", c["name"])
        high_sev = sum(1 for b in blocks if b["insight"]["severity"] == "high")
        
        result.append({
            "id": c["id"],
            "name": c["name"],
            "tier": c["tier"],
            "insight_count": len(blocks),
            "high_severity_count": high_sev
        })
        
    return result

@app.get("/api/competitors/{competitor_id}")
def competitor_detail(competitor_id: int):
    # Get name
    comp = next((c for c in DEMO_DATA["entities"]["competitors"] if c["id"] == competitor_id), None)
    if not comp:
        raise HTTPException(status_code=404, detail="Competitor not found")

    blocks = get_context_blocks_for_entity(competitor_id, "competitor", comp["name"])
    
    grouped = {
        "Theme": [],
        "GTM": [],
        "Positioning": [],
        "Uncategorized": []
    }
    
    for b in blocks:
        cat = b["insight"]["category"]
        if not cat: 
             cat = "Uncategorized"
        if cat not in grouped: # Handle 'Uncategorized' if strictly text
             cat = "Uncategorized"
             
        grouped[cat].append(b)
        
    return grouped

@app.get("/api/products")
def list_products():
    products = DEMO_DATA["entities"]["products"]
    result = []
    
    for p in products:
        blocks = get_context_blocks_for_entity(p["id"], "product", p["name"])
        
        result.append({
            "id": p["id"],
            "name": p["name"],
            "therapeutic_area": p["therapeutic_area"],
            "indication": p["indication"],
            "phase": p["phase"],
            "insight_count": len(blocks)
        })
        
    return result

@app.get("/api/products/{product_id}")
def product_detail(product_id: int):
    prod = next((p for p in DEMO_DATA["entities"]["products"] if p["id"] == product_id), None)
    if not prod:
         raise HTTPException(status_code=404, detail="Product not found")
         
    blocks = get_context_blocks_for_entity(product_id, "product", prod["name"])
    
    grouped = {
        "Direct": [],
        "Adjacent": []
    }
    
    for b in blocks:
        scope = b["insight"]["scope"]
        # Logic: If scope is 'product' -> Direct. If 'competitor' or 'market' or 'theme' -> Adjacent
        # Wait, usually scope='product' means it's about THIS product. 
        # But here logic is: Is the impact direct or adjacent?
        # Let's simplify: 
        # If insight.subjects contains THIS product name -> Direct
        # Else -> Adjacent
        
        # Check subjects
        subjects = b["insight"].get("subjects", [])
        if prod["name"] in subjects:
            cat = "Direct"
        else:
            cat = "Adjacent"
            
        grouped[cat].append(b)
        
    return grouped

if __name__ == "__main__":
    import uvicorn
    # Run on port 8000 to replace main app, or 8001 to run alongside?
    # User asked for a demo program. Let's update README to say "run this instead of main.py"
    # usage: python demo_main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
