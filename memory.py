import hashlib
import sqlite3
from datetime import datetime
from typing import List, Dict
import os

DB_NAME = "insight_pulse.db"

def fingerprint(signal: Dict) -> str:
    """Creates a unique hash for a signal based on content."""
    text = (signal.get("headline", "") + signal.get("description", "")).lower()
    return hashlib.md5(text.encode()).hexdigest()

def annotate_signals(signals: List[Dict]) -> List[Dict]:
    """Annotates signals with _seen_before and _last_seen from DB."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    for s in signals:
        fp = fingerprint(s)
        
        # Check if exists
        c.execute("SELECT last_seen FROM fingerprints WHERE hash = ?", (fp,))
        row = c.fetchone()
        
        if row:
            s["_seen_before"] = True
            s["_last_seen"] = row[0]
            # Update last_seen
            c.execute("UPDATE fingerprints SET last_seen = ? WHERE hash = ?", (now, fp))
        else:
            s["_seen_before"] = False
            s["_last_seen"] = None
            # Insert new
            c.execute("INSERT INTO fingerprints (hash, last_seen) VALUES (?, ?)", (fp, now))
            
    conn.commit()
    conn.close()
    return signals
