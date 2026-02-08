from typing import List, Dict
import database

def competitor_context_builder(
    insights: List[Dict], 
    competitor_id: int, 
    competitor_name: str
) -> List[Dict]:
    """
    Generates competitor-specific context blocks.
    
    Rules:
    - Include if scope is "competitor" OR "market".
    - Template: "This affects {competitor_name} because it reflects a change in their competitive environment related to: {insight.explanation}"
    """
    blocks = []
    
    # Filter scopes
    relevant_scopes = {"competitor", "market"}
    
    for insight in insights:
        # Step 4: Strict Subject Filtering
        subjects = insight.get("subjects", [])
        if competitor_name not in subjects:
            continue
            
        if insight.get("scope") in relevant_scopes:
            # Generate Framing
            explanation = insight.get("explanation", "")
            framing = f"Strategically relevant shift in the competitive environment for {competitor_name}."
            
            blocks.append({
                "insight_id": insight.get("id"), # Assumes Insight has ID from DB or upstream
                "focal_entity_id": competitor_id,
                "focal_entity_type": "competitor",
                "framing_text": framing
            })
            
    return blocks

def product_context_builder(
    insights: List[Dict], 
    product_id: int, 
    product_name: str
) -> List[Dict]:
    """
    Generates product-specific context blocks.
    
    Rules:
    - Include if scope is "product" OR "market".
    - Template: "This impacts {product_name} through market exposure to {insight.explanation}"
    """
    blocks = []
    
    # Filter scopes
    relevant_scopes = {"product", "market"}
    
    for insight in insights:
        # Step 4: Strict Subject Filtering
        subjects = insight.get("subjects", [])
        if product_name not in subjects:
            continue

        if insight.get("scope") in relevant_scopes:
            # Generate Framing
            explanation = insight.get("explanation", "")
            framing = f"Direct strategic or market exposure impacting {product_name}."
            
            blocks.append({
                "insight_id": insight.get("id"), 
                "focal_entity_id": product_id,
                "focal_entity_type": "product",
                "framing_text": framing
            })
            
    return blocks

# Removed standalone context_block_persistence to enforce single DB connection usage.

def build_and_store_context_blocks(insights: List[Dict], insight_ids: List[int], db, tenant_id: int):
    """
    Generates and stores context blocks for the given insights using the shared DB connection.
    """
    cursor = db.cursor()
    
    # Fetch Tenant Config (Exists check logic remains, but we use existing cursor)
    
    # Fetch Competitors
    comp_rows = cursor.execute("SELECT id, name FROM competitors WHERE tenant_id = ?", (tenant_id,)).fetchall()
    # Map name -> id for easier lookup, or just iterate. 
    # Function needs ID and Name.
    
    # Fetch Products
    prod_rows = cursor.execute("SELECT id, name FROM products WHERE tenant_id = ?", (tenant_id,)).fetchall()

    if len(insights) != len(insight_ids):
        return

    for i, ins in enumerate(insights):
        # Inject ID
        ins_with_id = ins.copy()
        ins_with_id["id"] = insight_ids[i]
        
        # Competitors
        for c_row in comp_rows:
            comp_name = c_row["name"] # c_row is sqlite3.Row or dict
            comp_id = c_row["id"]
            
            blocks = competitor_context_builder([ins_with_id], comp_id, comp_name)
            
            for block in blocks:
                 cursor.execute('''
                    INSERT INTO context_blocks (insight_id, focal_entity_id, focal_entity_type, framing_text)
                    VALUES (?, ?, ?, ?)
                ''', (
                    block["insight_id"], 
                    block["focal_entity_id"], 
                    block["focal_entity_type"], 
                    block["framing_text"]
                ))
                
        # Products
        for p_row in prod_rows:
            prod_name = p_row["name"]
            prod_id = p_row["id"]
            
            blocks = product_context_builder([ins_with_id], prod_id, prod_name)
            
            for block in blocks:
                 cursor.execute('''
                    INSERT INTO context_blocks (insight_id, focal_entity_id, focal_entity_type, framing_text)
                    VALUES (?, ?, ?, ?)
                ''', (
                    block["insight_id"], 
                    block["focal_entity_id"], 
                    block["focal_entity_type"], 
                    block["framing_text"]
                ))
    
    # No commit here? main.py calls commit() at end of process_pipeline?
    # Checked main.py: "db.commit()" is called after context building? 
    # Wait, main.py code:
    #   build_and_store_context_blocks(...)
    #   return {...}
    # It does NOT call commit() after this function! It called db.commit() after insight insert.
    # So we MUST commit here or main.py must change.
    # BUT wait, the `db` passed is `get_db()` which returns a connection.
    # If I use one connection, I can commit at the end of the transaction in `main.py`.
    # Let's check `main.py` again. 
    # It calls `db.commit()` after insights. Then calls `build_and_store...`. Then returns.
    # So context blocks are NOT committed in current `main.py`.
    # I should commit here, OR update main.py. 
    # "Context builder must NOT open its own DB connection." -> implies it uses the transaction.
    # I will commit here using `db.commit()` since I have the connection object.
    
    db.commit()
