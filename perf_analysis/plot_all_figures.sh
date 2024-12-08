#!/bin/bash

cd plot_scripts

echo "[INFO] Collating Results for Figure 14 and 15"
python3 generate_csv_fig14_15.py

echo "[INFO] Collating Results for Figure 16"
python3 generate_csv_fig16.py

echo "[INFO] Collating Results for Figure 17"
python3 generate_csv_fig17.py

echo "[INFO] Collating Results for Figure 18"
python3 generate_csv_fig18.py

echo "[INFO] Generating Figure 14"
python3 plot_fig14.py

echo "[INFO] Generating Figure 15"
python3 plot_fig15.py

echo "[INFO] Generating Figure 16"
python3 plot_fig16.py

echo "[INFO] Generating Figure 17"
python3 plot_fig17.py

echo "[INFO] Generating Figure 18"
python3 plot_fig18.py

cd ../