import os
import requests
import pandas as pd

# ENSURE OUTPUT DIRECTORY EXISTS
os.makedirs("data/raw",exist_ok=True)

def fetch_and_save_nav(scheme_code, filename):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for scheme code:{scheme_code}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # METADATA PARSING
        meta = data.get("meta", {})
        # HISTORICAL NAV PARSING
        nav_list = data.get("data",[])

        if not nav_list:
            print(f"No data found for scheme: {scheme_code}")
            return
        
        df = pd.DataFrame(nav_list)
        df["scheme_code"] = meta.get("scheme_code")
        df["scheme_name"] = meta.get("scheme_name")
        df["fund_house"]  = meta.get("fund_house")

        output_path = f"data/raw/{filename}.csv"
        df.to_csv(output_path, index=False)
        print(f"Successfully saved to {output_path}\n")

    except Exception as e:
        print(f"Error fetching {scheme_code}: {e}")

if __name__ == "__main__":
    # TASK 1: FETCH HDFC TOP 100 DIRECT
    fetch_and_save_nav(125497, "hdfc_top_100_live")

    # TASK 2: FETCH 5 KEY SCHEMES
    schemes = {
        119551: "sbi_bluechip",
        120503: "icici_bluechip",
        118632: "nippon_large_cap",
        119092: "axis_bluechip",
        120841: "kotak_bluechip"
    }

    for code, name in schemes.items():
        fetch_and_save_nav(code, f"key_scheme_{name}")
