from typing import List, Dict

def filter_signals(signals: List[Dict], tenant_config: Dict) -> List[Dict]:
    """
    Phase 2: Tenant Scoping Filter
    
    Strictly filters signals based on tenant configuration.
    
    Rules:
    1. KEEP if source_type == "regulatory" (Safety net)
    2. KEEP if company_mentions overlaps with tenant_config['competitors']
    3. KEEP if drug_mentions overlaps with tenant_config['products']
    4. DISCARD otherwise.
    
    Args:
        signals: List of event dictionaries (must have 'source_type', 'company_mentions', 'drug_mentions')
        tenant_config: Dict with 'competitors' (list of strings) and 'products' (list of strings)
        
    Returns:
        List of filtered signal dictionaries.
    """
    
    relevant_signals = []
    
    # Normalize config for case-insensitive matching
    tracked_competitors = {c.lower() for c in tenant_config.get("competitors", [])}
    tracked_products = {p.lower() for p in tenant_config.get("products", [])}
    
    for signal in signals:
        # Rule 1: Always keep regulatory
        if signal.get("source_type") == "regulatory":
            relevant_signals.append(signal)
            continue
            
        # Target text for searching
        headline = signal.get("headline", "").lower()
        description = signal.get("description", "").lower()
        content = headline + " " + description
            
        # Rule 2: Competitor overlap
        # Check explicit mentions OR string match in content
        company_mentions = {m.lower() for m in signal.get("company_mentions", [])}
        competitor_match = not company_mentions.isdisjoint(tracked_competitors)
        
        if not competitor_match:
            # Fallback: String search
            for comp in tracked_competitors:
                if comp in content:
                    competitor_match = True
                    break
        
        if competitor_match:
            relevant_signals.append(signal)
            continue
            
        # Rule 3: Product overlap
        drug_mentions = {d.lower() for d in signal.get("drug_mentions", [])}
        product_match = not drug_mentions.isdisjoint(tracked_products)
        
        if not product_match:
            # Fallback: String search
            for prod in tracked_products:
                if prod in content:
                    product_match = True
                    break
        
        if product_match:
            relevant_signals.append(signal)
            continue
            
        # Rule 4: Implicitly discard if no match
        
    return relevant_signals
