import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

def main():
    url = os.getenv("TECHOPS_DATABASE_URL")
    if not url:
        raise SystemExit("Set TECHOPS_DATABASE_URL first.")
    csv_path = Path(__file__).resolve().parents[1] / "data" / "incidents.csv"
    df = pd.read_csv(csv_path)
    engine = create_engine(url)
    df.to_sql("incidents", engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into PostgreSQL table incidents.")

if __name__ == "__main__":
    main()
