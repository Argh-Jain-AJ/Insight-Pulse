import requests
import time
import sys

# Conceptual Automatic Trigger for Insight Pulse
# This script demonstrates how the system can be integrated with external 
# schedulers (cron), CI/CD webhooks, or cloud triggers.

API_URL = "http://127.0.0.1:8000/api/process"
TENANT_ID = 1  # Standard demo tenant

def trigger_ingestion():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Triggering automatic ingestion for Tenant {TENANT_ID}...")
    try:
        response = requests.post(f"{API_URL}?tenant_id={TENANT_ID}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Insights generated: {result.get('insights_generated', 0)}")
        else:
            print(f"Failed to trigger. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the uvicorn server is running.")

if __name__ == "__main__":
    # In a real-world scenario, this script could be:
    # 1. Called by a CRON job every 6 hours.
    # 2. Run in a continuous loop with a sleep timer (shown below).
    # 3. Triggered by a webhook from a data source.
    
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        print("Starting in loop mode (every 1 hour)...")
        while True:
            trigger_ingestion()
            time.sleep(3600)  # Wait for 1 hour
    else:
        # Single execution (default)
        trigger_ingestion()
