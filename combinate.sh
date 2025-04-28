#!/bin/bash

head -n 1 vendor_efficiency_1.csv > vendor_efficiency_summary.csv
for file in vendor_efficiency_*.csv; do
  if [ "$file" != "vendor_efficiency_summary.csv" ]; then
    tail -n +2 "$file" >> vendor_efficiency_summary.csv
  fi
done
