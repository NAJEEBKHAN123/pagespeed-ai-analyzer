# check_data.py
import pandas as pd
import os

print("Checking data...")

data_path = "data/raw/sample_data.csv"
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    print(f"✅ Data file exists with {len(df)} rows")
    print(f"✅ Columns: {list(df.columns)}")
    print("\n📋 First 3 rows:")
    print(df.head(3))
    
    # Check for empty rows
    if len(df) == 0:
        print("❌ WARNING: File exists but has 0 rows!")
    else:
        print(f"✅ Data looks good! {len(df)} rows loaded.")
else:
    print(f"❌ Data file not found at {data_path}")