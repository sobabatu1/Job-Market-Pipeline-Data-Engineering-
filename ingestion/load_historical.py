import pandas as pd
from sqlalchemy import create_engine, text  # Add 'text' here
import os
import urllib.parse

# 1. Properly encode the password
password = urllib.parse.quote_plus("Olayinka@1")
DB_URL = f"postgresql://postgres:{password}@localhost:5432/job_pipeline"
engine = create_engine(DB_URL)

def load_bronze():
    # 2. Wrap raw SQL strings in text()
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS marts;"))
        conn.commit()  # In SQLAlchemy 2.0, you often need an explicit commit
        print("✅ Schemas created: raw, staging, marts")

    # 3. Load Job Postings in Chunks
    file_path = 'data/raw/job_postings.csv'
    chunk_size = 50000 
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"🚀 Starting load for {file_path}...")
    
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        mode = 'replace' if i == 0 else 'append'
        # pandas .to_sql handles the execution logic internally, 
        # so no changes are needed here.
        chunk.to_sql('job_postings', engine, schema='raw', if_exists=mode, index=False)
        print(f"  Loaded chunk {i+1} ({(i+1)*chunk_size} rows)...")

    print("✅ Bronze layer load complete!")

if __name__ == "__main__":
    load_bronze()