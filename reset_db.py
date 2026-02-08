import sqlite3
import os

DB_NAME = "insight_pulse.db"

def reset_db():
    if not os.path.exists(DB_NAME):
        print(f"Database {DB_NAME} not found. Nothing to reset.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    tables = ["fingerprints", "insights", "context_blocks", "events"]
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")
        except sqlite3.OperationalError as e:
            print(f"Error clearing table {table} (it might not exist): {e}")
            
    conn.commit()
    conn.close()
    print("Database reset complete.")

if __name__ == "__main__":
    reset_db()
