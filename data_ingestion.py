import os
import glob
import pandas as pd

def ingest_and_explore_raw_csv():
    print("=== Exploring 10 csv Datasets ===")
    csv_files = glob.glob("data/raw/*.csv")

    if not csv_files:
        print("No CSV files found in data/raw/. please add your 10 source files.")
        return
    
    for file in csv_files[:10]: # LIMITS TO FIRST 10 FOR INSPECTION
        print("=" * 50)
        print(f"\n---File:{file}---")
        df = pd.read_csv(file)
        print(f"Shape: {df.shape[0]} rows and {df.shape[1]} columns")
        print("-" * 50)
        print("\nData Types:")
        print(df.dtypes)
        print("-" * 50)
        print("\nSample Data:")
        print(df.head(3))
        

        # QUICK ANOMALY CHECK
        missing = df.isnull().sum().sum()
        dupes = df.duplicated().sum()
        if missing > 0 or dupes > 0:
            print(f"Anomalies detected:{missing} missing values, {dupes} duplicate rows.")

def explore_fund_master(fund_master_path):
    print("\n == Exploring Fund Master ===")
    if not os.path.exists(fund_master_path):
        print(f"Fund Master file not found at {fund_master_path}")
        return None
    
    df = pd.read_csv(fund_master_path)

    # CHECK EXPECTED UNIQUE FIELDS (ADJUST COLUMN NAMES BASED ON YOUR FILE)
    cols = df.columns
    print(f"Available Columns : {list(cols)}")

    for col in ["fund_house", "category", "sub_category", "risk_grade"]:
        if col in df.columns:
            print(f"\nUnique Values in '{col}'(Top 5)")
            print(df[col].unique()[:5])

        return df

def validate_amfi_codes(fund_master_df, nav_history_path):
    print("\n=== Step 3: Data Quality Validation ===")
    if fund_master_df is None or not os.path.exists(nav_history_path):
        print("Validation Skipped due to missing files.")
        return
    
    nav_df = pd.read_csv(nav_history_path)

    # USING 'amfi_code' TO LINK BOTH TABLES

    master_codes = set(fund_master_df['amfi_code'].unique())
    nav_codes = set(nav_df['amfi_code'].unique())

    missing_in_nav = master_codes - nav_codes

    print("--- DQ Summary ---")
    print(f"Total codes in Fund Master: {len(master_codes)}")
    print(f"Total Unique codes in NAV History : {len(nav_codes)}")
    if missing_in_nav:
        print(f"DQ Altert: {len(missing_in_nav)} codes in Fund MAster have No Matching history")
        print(f"Sample Missing codes: {list(missing_in_nav)[:5]}")
    else:
        print(f"DQ pass: Every AMFI code in fund_master exists in nav_history")

    

if __name__ == "__main__":
    # 1. INGEST & PROFILE
    ingest_and_explore_raw_csv()

    # 2 & 3   MASTER EXPLORATION & VALIDATION
    # (ADJUST "fund_master.csv" AND "nav_history.csv" to match your actual names)
    master_df = explore_fund_master("data/raw/01_fund_master.csv")
    validate_amfi_codes(master_df, "data/raw/02_nav_history.csv")

