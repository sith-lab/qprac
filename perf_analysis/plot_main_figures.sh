#!/bin/bash

cd plot_scripts

echo "[INFO] Collating Results for Figure 14 and 15 "
python3 generate_csv_fig14_15.py

echo "[INFO] Generating Figure 14"
python3 plot_fig14.py

echo "[INFO] Generating Figure 15"
python3 plot_fig15.py

cd ../