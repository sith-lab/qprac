#!/bin/bash

cd plot_scripts

echo "[INFO] Collating Results for Figure 19"
bash generate_csv_fig19.sh

echo "[INFO] Collating Results for Figure 20"
python3 generate_csv_fig20.py

echo "[INFO] Generating Figure 19"
python3 plot_fig19.py

echo "[INFO] Generating Figure 20"
python3 plot_fig20.py

cd ../