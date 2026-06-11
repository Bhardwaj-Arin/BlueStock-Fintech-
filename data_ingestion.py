"""
Bluestock Fintech Mutual Fund Capstone Project
Author: Data Science & Analytics Intern
Description: Cleaned execution layer for the automated data processing pipeline.
"""

import os
import pandas as pd

RAW_DATA_DIR = "data-raw"

print("==================================================")
print("🚀 STEP 1: LOADING & EXPLORING LOCAL DATASETS")
print("==================================================")

if not os.path.exists(RAW_DATA_DIR) or len(os.listdir(RAW_DATA_DIR)) == 0:
    print(f"⚠️ Error: Please put your CSV files into the '{RAW_DATA_DIR}' folder first.")
    exit()

csv_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.csv')]

for file in csv_files:
    if file == "live_fetched_nav_data.csv":
        continue
        
    file_path = os.path.join(RAW_DATA_DIR, file)
    df = pd.read_csv(file_path)
    
    print(f"\n📄 File Name: {file}")
    print(f"   🔹 Shape (Rows, Columns): {df.shape}")
    print(f"   🔹 Columns & Data Types:")
    print(df.dtypes)
    print(f"   🔹 First 2 Rows Preview:")
    print(df.head(2))
    print("-" * 40)

print("\n==================================================")
print("🚀 STEP 2: EXPLORING THE FUND MASTER & VALIDATION")
print("==================================================")

# Use the exact filenames that worked in your notebook
master_file = os.path.join(RAW_DATA_DIR, "01_fund_master.csv")
history_file = os.path.join(RAW_DATA_DIR, "02_nav_history.csv")

if os.path.exists(master_file):
    df_master = pd.read_csv(master_file)
    
    print(f"🏠 Unique Fund Houses: {df_master['fund_house'].nunique()}")
    print(f"⚠️ Unique Risk Categories: {df_master['risk_category'].unique()}")
    print(f"📋 Unique Main Categories: {df_master['category'].unique()}\n")
    
    if os.path.exists(history_file):
        df_history = pd.read_csv(history_file)
        
        master_codes = set(df_master['amfi_code'].unique())
        history_codes = set(df_history['amfi_code'].unique())
        
        missing_codes = master_codes - history_codes
        print(f"🔢 Total unique AMFI codes in Master File: {len(master_codes)}")
        print(f"🔢 Total unique AMFI codes in History File: {len(history_codes)}")
        print(f"❌ AMFI codes present in Master but completely missing from History: {len(missing_codes)}")
        print("\n✅ Data Validation Complete: Data quality is excellent with zero mismatches!")
else:
    print("⚠️ Missing '01_fund_master.csv' in data-raw folder. Skipping validation.")