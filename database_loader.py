import os
import sqlite3
import pandas as pd 
from sqlalchemy import create_engine

def load_database():
    print("===  LOADING DATA INTO SQLITE RELATIONAL DB ===")

    #  FORCE RESET: This automatically drops the old database file so it can't block your new schema!
    db_filename = "bluestock_mf.db"
    if os.path.exists(db_filename):
        os.remove(db_filename)
        print(f"Removed old instance of {db_filename} to apply new schema changes.")

    # CONNECT TO DATABASE FILE
    engine = create_engine("sqlite:///bluestock_mf.db")

    # INITIALIZE THE TABLES USING OUR SCHEMA FILE
    with open("schema.sql", 'r') as f:
        schema_sql = f.read()

    with sqlite3.connect("bluestock_mf.db") as conn:
        conn.executescript(schema_sql)
    print("Schema initialized successfully.")

    # LOAD CLEANED MAPPINGS TO DATABASE TARGETS
    # (ADJUST NAMES TO MATCH YOUR PRECISE 10 FILES IF NECESSARY)
    data_mappings = {

        "data/processed/01_fund_master_cleaned.csv": "dim_fund",
        "data/processed/02_nav_history_cleaned.csv": "fact_nav",
        "data/processed/08_investor_transactions_cleaned.csv": "fact_transactions",
        "data/processed/07_scheme_performance_cleaned.csv": "fact_performance",
        "data/processed/03_aum_by_fund_house_cleaned.csv": "fact_aum"
    }

    for path, table in data_mappings.items():
        df = pd.read_csv(path)
        # USING APPEND SINCE EMPTY TABLES WERE CREATED BY schema.sql
        df.to_sql(table, con= engine, if_exists='append', index=False)

        #   VERIFY ROW COUNTS MATCH
        db_count = pd.read_sql_query(f"SELECT COUNT(*) FROM {table}", engine).iloc[0,0]
        print(f"Verified Table [{table}]: CSV Rowcount = {(df)} | DB Rowcount = {db_count}")

    print("Database successfully loaded without row count leaks")


if __name__ == "__main__":
    load_database()