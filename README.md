## info
This GitHub repository works for the University of Wisconsin–Madison course STAT405 spring2025 final project- group4.

**Memeber: Ella Gruen, Anthony Pagas, John Chumlea, Shien Zhu and Samuel Negus**

Keys: Linux, emacs, HTC, NYC taxi

We conduct an analysis on answering which taxi vendor is the most time efficient to take during any day of the week.

### get data
https://www.kaggle.com/datasets/chilam/nyctaxis

### structure
- `efficiency_all.py`: a primary python file we used for doing the basic computation of vendor efficiency, at the HTC nodes.
- `efficiency_df.py`: a pyhton file that does the basic computation of vendor efficiency at the local machine.
- `submit_all.sh`: a shell script that allows Python files to do computation for data in a pre-set R container at the HTC nodes.
- `efficiency_0426.sub`: a shell script that submits 12 parallel jobs to run `efficiency_all.py`, `submit_all.sh` to HTC nodes.
- `names.list`: give a queue list for `efficiency_0426.sh` submitting the jobs.
- `vendor_efficiency_*.csv`: the cleaned computed results `.csv` files.
- `combine.sh`: combine all `vendor_efficiency_*.csv` to `vendor_efficiency_summary.csv`
