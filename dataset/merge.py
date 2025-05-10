# dataset/merge.py

import os
import pandas as pd
from config import CSV_OUTPUT_DIR

def merge_csvs(output_file="merged_dataset.csv"):
    csv_files = [f for f in os.listdir(CSV_OUTPUT_DIR) if f.endswith(".csv")]
    dfs = [pd.read_csv(os.path.join(CSV_OUTPUT_DIR, f)) for f in csv_files]
    df_combined = pd.concat(dfs, ignore_index=True)
    df_combined.to_csv(os.path.join(CSV_OUTPUT_DIR, output_file), index=False)
    print(f"[INFO] Merged dataset saved to {output_file}")
