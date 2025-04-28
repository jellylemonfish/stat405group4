#!/bin/bash

echo "Job running on $(hostname)"

# send the csv from staging into container
f="$1"
f_in_container="${f/\/staging\/groups\/stat_dscp\/group04/\/mnt\/data}"

apptainer exec \
  --bind /staging/groups/stat_dscp/group04:/mnt/data \
  /staging/groups/stat_dscp/group04/python_numpy_pandas_sklearn.sif \
  python3 efficiency_all.py "$f_in_container"
