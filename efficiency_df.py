## the first version for one-job submit
## and it could be run successfully locally

import pandas as pd
import glob

# List all trip_data CSVs
files = sorted(glob.glob("trip_data_*.csv"))
all_dfs = []

# Distance bin setup
bins = [0, 1, 3, 6, 10, float("inf")]
labels = ["0–1mi", "1–3mi", "3–6mi", "6–10mi", "10mi+"]

for file in files:
    df = pd.read_csv(file)
    
    # Convert pickup time
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    df = df.dropna(subset=["pickup_datetime"])
    
    # Remove bad trips
    df = df[(df["trip_time_in_secs"] > 0) & (df["trip_distance"] > 0)]
    
    # Feature engineering
    df["hour"] = df["pickup_datetime"].dt.hour
    df["dayofweek"] = df["pickup_datetime"].dt.dayofweek
    df["distance_bin"] = pd.cut(df["trip_distance"], bins=bins, labels=labels)
    
    # Minutes per mile
    df["minutes_per_mile"] = df["trip_time_in_secs"] / 60 / df["trip_distance"]
    
    all_dfs.append(df)

# Combine all
full_df = pd.concat(all_dfs, ignore_index=True)

# Group and aggregate
grouped = (
    full_df.groupby(["vendor_id", "distance_bin", "hour", "dayofweek"])
    ["minutes_per_mile"]
    .mean()
    .reset_index()
)

# Save result
grouped.to_csv("vendor_efficiency_summary.csv", index=False)

