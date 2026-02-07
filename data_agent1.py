import requests
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load Environment Variables from .env
load_dotenv()

# API Keys (Replace with .env or secure config in production)
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

# =========================================================================
# DATA AGENT 1: Raw Event Ingestion Node
# =========================================================================
# This node is responsible for fetching raw data from disparate pharma 
# and market signals sources. 
#
# Sources:
# 1. NewsAPI (Market/Competitor News)
# 2. openFDA (Adverse Events/Regulatory)
# 3. Europe PMC (Clinical/Research Articles)
# 4. USPTO PatentsView (Patent Filings)
#
# Note: This is a pure function/pipeline node, NOT a LangChain tool.
# It must run outside agent authority logic to maintain clean data-before-reasoning boundary.

def event_ingestion_node(query: str, competitors: List[str] = None, products: List[str] = None) -> dict:
    """
    Event Ingestion Node.
    Fetches raw events from multiple sources and normalizes into event schema.
    
    Now performs targeted searches for each competitor and product if provided.
    """

    if competitors is None: competitors = []
    if products is None: products = []
    
    # Combine entities for broad search
    all_entities = list(set(competitors + products))
    if not all_entities and query:
        all_entities = [query]
    elif not all_entities:
        all_entities = ["pharmaceutical"]

    events: List[Dict] = []
    seen_urls = set()
    sources_checked = 0
    collected_at = datetime.utcnow().isoformat()

    # =========================================================================
    # 1. NEWSAPI — TARGETED PHARMA NEWS
    # =========================================================================
    sources_checked += 1

    if NEWSAPI_KEY:
        for entity in all_entities:
            try:
                response = requests.get(
                    "https://newsapi.org/v2/everything",
                    params={
                        "q": entity,
                        "apiKey": NEWSAPI_KEY,
                        "language": "en",
                        "pageSize": 5, 
                        "sortBy": "publishedAt"
                    },
                    timeout=10
                )

                if response.status_code != 200:
                    continue

                articles = response.json().get("articles", [])
                for a in articles:
                    url = a.get("url")
                    if not url or url in seen_urls:
                        continue

                    seen_urls.add(url)
                    events.append({
                        "source": a.get("source", {}).get("name", "NewsAPI"),
                        "source_type": "news",
                        "event_type": "news_article",
                        "published_at": a.get("publishedAt", ""),
                        "collected_at": collected_at,
                        "headline": a.get("title", ""),
                        "description": a.get("description", "") or a.get("title", ""),
                        "url": url,
                        "raw_json": a
                    })
            except Exception as e:
                print(f"NewsAPI error for {entity}:", e)
    else:
        print("NEWSAPI_KEY not set")

    # =========================================================================
    # 2. openFDA — TARGETED ADVERSE EVENTS
    # =========================================================================
    sources_checked += 1

    for entity in all_entities:
        try:
            response = requests.get(
                "https://api.fda.gov/drug/event.json",
                params={
                    "search": f'patient.drug.medicinalproduct:"{entity}"',
                    "limit": 5
                },
                timeout=10
            )

            if response.status_code != 200:
                continue

            fda_events = response.json().get("results", [])
            for fda_event in fda_events:
                drugs = []
                reactions = []
                patient = fda_event.get("patient", {})
                
                for d in patient.get("drug", []):
                    name = d.get("medicinalproduct")
                    if name: drugs.append(name)

                for r in patient.get("reaction", []):
                    reaction = r.get("reactionmeddrapt")
                    if reaction: reactions.append(reaction)

                description = f"FDA report for {entity}. Drugs: {', '.join(drugs[:2])}. Reactions: {', '.join(reactions[:3])}."

                events.append({
                    "source": "openFDA",
                    "source_type": "regulatory",
                    "event_type": "adverse_event",
                    "published_at": fda_event.get("receiptdate", ""),
                    "collected_at": collected_at,
                    "headline": f"Targeted FDA Report: {entity}",
                    "description": description,
                    "url": "https://open.fda.gov",
                    "drug_mentions": drugs,
                    "raw_json": fda_event
                })
        except Exception as e:
            print(f"openFDA error for {entity}:", e)

    # =========================================================================
    # 3. EUROPE PMC — TARGETED RESEARCH
    # =========================================================================
    sources_checked += 1

    for entity in all_entities:
        try:
            pmc_response = requests.get(
                "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
                params={
                    "query": entity,
                    "format": "json",
                    "pageSize": 5
                },
                timeout=10
            )

            if pmc_response.status_code != 200:
                continue

            articles = pmc_response.json().get("resultList", {}).get("result", [])
            for art in articles:
                url = art.get("doi") or art.get("id")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                
                events.append({
                    "source": art.get("journalTitle", "Europe PMC"),
                    "source_type": "journal",
                    "event_type": "research_article",
                    "published_at": art.get("firstPublicationDate", ""),
                    "collected_at": collected_at,
                    "headline": art.get("title", ""),
                    "description": art.get("abstractText", "")[:300] if art.get("abstractText") else art.get("title", ""),
                    "url": f"https://doi.org/{url}" if art.get("doi") else "https://europepmc.org",
                    "raw_json": art
                })
        except Exception as e:
            print(f"Europe PMC error for {entity}:", e)

    # =========================================================================
    # 4. USPTO PATENTSVIEW — TARGETED PATENTS
    # =========================================================================
    sources_checked += 1

    for entity in all_entities:
        try:
            patent_query = {
                "q": {"_text_any": {"patent_title": entity}},
                "f": ["patent_title", "patent_date", "patent_abstract", "assignees.assignee_organization"],
                "o": {"per_page": 5}
            }
            response = requests.post("https://api.patentsview.org/patents/query", json=patent_query, timeout=10)
            
            if response.status_code != 200:
                continue

            patents = response.json().get("patents", [])
            for p in patents:
                title = p.get("patent_title", "")
                if title in seen_urls: continue 
                seen_urls.add(title)

                events.append({
                    "source": "USPTO PatentsView",
                    "source_type": "patent",
                    "event_type": "patent_filing",
                    "published_at": p.get("patent_date", ""),
                    "collected_at": collected_at,
                    "headline": title,
                    "description": p.get("patent_abstract", "")[:300] if p.get("patent_abstract") else title,
                    "url": "https://patentsview.org",
                    "company_mentions": [a.get("assignee_organization") for a in p.get("assignees", [])],
                    "raw_json": p
                })
        except Exception as e:
            print(f"USPTO error for {entity}:", e)

    return {
        "events": events,
        "ingestion_metadata": {
            "query": query,
            "sources_checked": sources_checked,
            "events_collected": len(events),
            "collected_at": collected_at
        },
        "timestamp": collected_at
    }

# Backward compatibility alias
data_agent = event_ingestion_node