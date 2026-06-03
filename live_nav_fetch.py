import os
import requests
import pandas as pd

RAW_DATA_DIR = "data-raw"

target_schemes = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

print("🌐 Starting live NAV data extraction from api.mfapi.in...")
all_records = []

for code, name in target_schemes.items():
    api_url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        json_data = response.json()
        meta = json_data.get('meta', {})
        prices = json_data.get('data', [])
        
        for item in prices:
            all_records.append({
                "amfi_code": code,
                "scheme_name": meta.get('scheme_name'),
                "date": item.get('date'),
                "nav": item.get('nav')
            })
        meta = json_data.get('meta', {})
        prices = json_data.get('data', [])
        
        for item in prices:
            all_records.append({
                "amfi_code": code,
                "scheme_name": meta.get('scheme_name'),
                "date": item.get('date'),
                "nav": item.get('nav')
            })
        print(f"   ✅ Fetched records for: {name}")

# Convert list to DataFrame and save cleanly in the project directory
live_df = pd.DataFrame(all_records)
output_path = os.path.join(RAW_DATA_DIR, "live_fetched_nav_data.csv")
live_df.to_csv(output_path, index=False)

print(f"\n🎉 Done! All live data safely stored in {output_path}")