import pandas as pd
import glob
import os
import sys

# List all trip_data CSVs
#files = sorted(glob.glob("trip_data_*.csv"))
files = [sys.argv[1]]

all_dfs = []

# Distance bin setup
bins = [0, 1, 3, 6, 10, float("inf")]
labels = ["0–1mi", "1–3mi", "3–6mi", "6–10mi", "10mi+"]

for file in files:
   # df = pd.read_csv(file)
   # df = pd.read_csv(file, low_memory=False, dtype=str)
    chunks = pd.read_csv(file, chunksize=100_000, low_memory=False, dtype=str)

    for chunk in chunks:
        # Keep the head of csv 
        chunk.columns = chunk.columns.str.strip()
        
        # Convert relevant columns
        chunk["trip_distance"] = pd.to_numeric(chunk["trip_distance"], errors="coerce")
        chunk["trip_time_in_secs"] = pd.to_numeric(chunk["trip_time_in_secs"], errors="coerce")
        
        # Convert pickup time
        chunk["pickup_datetime"] = pd.to_datetime(chunk["pickup_datetime"], errors="coerce")
        chunk = chunk.dropna(subset=["pickup_datetime"])

        # Remove bad trips
        chunk = chunk[(chunk["trip_time_in_secs"] > 0) & (chunk["trip_distance"] > 0)]

        # Feature engineering
        chunk["hour"] = chunk["pickup_datetime"].dt.hour
        chunk["dayofweek"] = chunk["pickup_datetime"].dt.dayofweek
        chunk["distance_bin"] = pd.cut(chunk["trip_distance"], bins=bins, labels=labels)
        
        # Minutes per mile
        chunk["minutes_per_mile"] = chunk["trip_time_in_secs"] / 60 / chunk["trip_distance"]
        
        # Group and aggregate
        grouped = (
            chunk.groupby(["vendor_id", "distance_bin", "hour", "dayofweek"], observed=False)
            ["minutes_per_mile"]
            .mean()
            .reset_index()
        )
        all_dfs.append(grouped)


# Combine all
full = pd.concat(all_dfs).groupby(
    ["vendor_id", "distance_bin", "hour", "dayofweek"]
)["minutes_per_mile"].mean().reset_index()


# Save result
# old version: full.to_csv("vendor_efficiency_summary.csv", index=False)

# Save the the result as vendor_efficiency_*.csv, combinate as a big csv with another new .sh script
output = "vendor_efficiency_" + os.path.basename(files[0]).split("_")[-1].replace(".csv", "") + ".csv"
full.to_csv(output, index=False)
