# etl/db_ingest.py
"""
Simple ingestion: reads processed CSV and writes to SQL table trade_clean using SQLAlchemy.
Supports Postgres by default (change connection URL for other DBs).
"""
import pandas as pd
from sqlalchemy import create_engine, text
import os

def ingest_to_db(processed_csv_path: str, db_url: str, table_name: str = 'trade_clean', if_exists: str = 'replace'):
    df = pd.read_csv(processed_csv_path)
    engine = create_engine(db_url, pool_pre_ping=True)

    # basic type conversions can be applied here if needed
    with engine.begin() as conn:
        # create target schema if necessary (example for Postgres)
        df.to_sql(table_name, conn, if_exists=if_exists, index=False, method='multi', chunksize=1000)
    print(f"Ingested {len(df)} rows into {table_name} at {db_url}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='../outputs/processed_trade_sample.csv')
    parser.add_argument('--db', required=False, help='SQLAlchemy DB URL, e.g. postgresql+psycopg2://user:pass@host:5432/dbname')
    parser.add_argument('--table', default='trade_clean')
    args = parser.parse_args()

    db_url = args.db or os.getenv('DATABASE_URL')
    if not db_url:
        raise SystemExit("Provide --db or set DATABASE_URL env var.")
    ingest_to_db(args.csv, db_url, args.table)
