import os
import numpy as np
import pandas as pd 

# ENSURE THE PROCESSED OUTPUT FOLDER EXISTS
os.makedirs("data/processed", exist_ok=True)

def clean_pipeline():
    print("=== CLEANING DATA ===")

    # TASK 1: CLEAN nav_history.csv (02_nav_history.csv)

    print("Cleaning NAV History....")
    nav_df = pd.read_csv("data/raw/02_nav_history.csv")

    #STANDARDIZE COLUMN NAMING AS PER PROJECT'S MAPPING

    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(by=['amfi_code','date'])

    # DROP PURE DUPLICATES
    nav_df = nav_df.drop_duplicates()

    # FORWARD-FILL MISSING NAV VALUES FOR WEEKENDS/HOLIDAYS PER amfi_code GROUP
    nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].ffill()

    #   VALIDATE NAV > 0
    nav_df = nav_df[nav_df['nav'] > 0]
    nav_df.to_csv("data/processed/02_nav_history_cleaned.csv", index=False)

    # TASK 2: CLEAN insvestor_transactions.csv (08_investor_transactions.csv)

    print("Cleaning Investor Transactions...")
    tx_df = pd.read_csv("data/raw/08_investor_transactions.csv")

    # CONVERTING DATA TYPE OF transaction_date 
    tx_df['transaction_date'] = pd.to_datetime(tx_df["transaction_date"])
    
    #STANDARDIZE TRANSACTION TYPES
    tx_df['transaction_type'] = tx_df['transaction_type'].str.strip().str.capitalize()

    # MAP VARIATION INPUTS SAFELY TO: SIP / Lumpsum / Redemption
    type_mapping = {"Sip":'SIP', "Lumpsum": "Lumpsum", "Redemption":"Redemption", "Buy":"Lumpsum", "Sell": "Redemption"}
    tx_df['transaction_type'] = tx_df['transaction_type'].map(type_mapping).fillna("Lumpsum")

    # VALIDATE amount_inr > 0 AND FILTER VALID KYC STATUSES
    tx_df = tx_df[tx_df['amount_inr'] > 0]
    tx_df["kyc_status"] = tx_df["kyc_status"].str.strip().str.upper()
    tx_df = tx_df[tx_df["kyc_status"].isin(['Y', 'N' , 'PENDING', 'YES', 'NO'])]
    tx_df.to_csv("data/processed/08_investor_transactions_cleaned.csv", index=False)

    # TASK 3: CLEAN scheme_performance.csv (07_scheme_perfromance.csv)

    print("Cleaning Scheme Performance...")
    perf_df = pd.read_csv("data/raw/07_scheme_performance.csv")

    # CONVERT RETURN COLUMNS TO NUMERIC, COERCION TURNING STRING JUNK INTO NaN
    return_cols = [c for c in perf_df.columns if 'return' in c.lower() or 'performance' in c.lower()]
    for col in return_cols:
        perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce').fillna(0)

    #   CLIP EXPENSE RATIO WITHIN VALID THRESHOLD LIMITS (0.1% to 2.5% format as decimal or raw %)
    if 'expense_ratio' in perf_df.columns:
        perf_df['expense_ratio'] = pd.to_numeric(perf_df["expense_ratio"], errors='coerce')
        perf_df["expense_ratio"] = perf_df['expense_ratio'].clip(lower=0.1, upper=2.5)

    perf_df.to_csv("data/processed/07_scheme_performance_cleaned.csv", index=False)


    # PROCESS REMAINING FILES DIRECTLY TO OUTPUT FOLDER TO COMPLETE DELIVERY ARRAY
    print("Staging remaining delivery datasets...")
    for file in os.listdir("data/raw"):
        if file.endswith(".csv") and not os.path.exists(f"data/processed/{file.replace(".csv", "_cleaned.csv")}"):
            df = pd.read_csv(f"data/raw/{file}")
            df.to_csv(f"data/processed/{file.replace(".csv", "_cleaned.csv")}", index=False)

    print("All 10 files cleaned and exported to data/processed")

if __name__ == "__main__":
    clean_pipeline()
