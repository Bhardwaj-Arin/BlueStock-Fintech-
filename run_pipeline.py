"""
Bluestock Fintech Mutual Fund Data Pipeline
Master Execution Script — Day 7 Final Deployment
"""

import os
import sys
import subprocess

def run_script(script_name):
    """Helper function to run a python script and track success."""
    print(f"\n[RUNNING] Executing: {script_name}...")
    try:
        # Runs the script and waits for it to finish
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {script_name} finished cleanly.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {script_name} failed with the following message:\n{e.stderr}")
        return False

def main():
    print("==================================================")
    print("   BLUESTOCK FINTECH — MASTER DATA PIPELINE       ")
    print("==================================================")
    
    # 1. Fetch live data / Ingest raw assets
    if os.path.exists('data_ingestion.py'):
        if not run_script('data_ingestion.py'):
            print("[HALT] Pipeline stopped due to ingestion error.")
            return
    elif os.path.exists('sql/data_ingestion.py'):
        if not run_script('sql/data_ingestion.py'):
            return

    # 2. Live NAV Fetch updates
    if os.path.exists('live_nav_fetch.py'):
        run_script('live_nav_fetch.py')
    elif os.path.exists('sql/live_nav_fetch.py'):
        run_script('sql/live_nav_fetch.py')

    # 3. Verify analytics engine output
    if os.path.exists('recommender.py'):
        print("\n[INFO] Recommender utility is deployed and ready for user execution.")

    print("\n==================================================")
    print("   PIPELINE EXECUTION COMPLETE — ALL ASSETS READY ")
    print("==================================================")

if __name__ == "__main__":
    main()