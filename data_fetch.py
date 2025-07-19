import pandas as pd
import os
import sqlite3
from datetime import datetime, timedelta

# Optional: import entsoe-py if you have an API key
try:
    from entsoe import EntsoePandasClient
    ENTSOE_ENABLED = True
except ImportError:
    ENTSOE_ENABLED = False

# === CONFIGURATION ===
ELIA_RAW_DIR = "data/raw"
SQLITE_DB = "data/grid_data.sqlite"
COUNTRY_CODE = "BE"  # Belgium
START_DATE = pd.Timestamp("2023-01-01", tz="Europe/Brussels")
END_DATE = pd.Timestamp("2023-12-31", tz="Europe/Brussels")
ENTSOE_API_KEY = os.getenv("ENTSOE_API_KEY")  # Set this in your environment
os.makedirs("data", exist_ok=True)

# === FUNCTIONS ===

def load_elia_csv(name):
    file_path = os.path.join(ELIA_RAW_DIR, name)
    df = pd.read_csv(file_path, sep=";", parse_dates=["Datetime (UTC)"], dayfirst=True)
    df.rename(columns={"Datetime (UTC)": "timestamp_utc"}, inplace=True)
    df["timestamp_be"] = pd.to_datetime(df["timestamp_utc"]).dt.tz_localize("UTC").dt.tz_convert("Europe/Brussels")
    return df

def fetch_entsoe_load():
    if not ENTSOE_ENABLED or not ENTSOE_API_KEY:
        return None
    client = EntsoePandasClient(api_key=ENTSOE_API_KEY)
    print("Fetching ENTSO-E load data...")
    df = client.query_load(COUNTRY_CODE, START_DATE, END_DATE)
    df = df.reset_index()
    df.columns = ["timestamp_be", "load_mw"]
    df["timestamp_be"] = df["timestamp_be"].dt.tz_convert("Europe/Brussels")
    return df

def save_to_sqlite(df, table_name):
    with sqlite3.connect(SQLITE_DB) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

# === MAIN ===

print("Loading Elia ODS002 (load forecast/actual)...")
df_load = load_elia_csv("ods002.csv")
save_to_sqlite(df_load, "elia_load")

print("Loading Elia ODS003 (load on Elia grid)...")
df_grid_load = load_elia_csv("ods003.csv")
save_to_sqlite(df_grid_load, "elia_grid_load")

print("Loading Elia ODS201 (generation mix)...")
df_gen = load_elia_csv("ods201.csv")
save_to_sqlite(df_gen, "elia_generation")

if ENTSOE_ENABLED and ENTSOE_API_KEY:
    df_entsoe = fetch_entsoe_load()
    if df_entsoe is not None:
        save_to_sqlite(df_entsoe, "entsoe_load")
else:
    print("ENTSO-E API key not set or library not installed — skipping ENTSO-E fetch.")

print("✅ All data processed and saved to:", SQLITE_DB)
