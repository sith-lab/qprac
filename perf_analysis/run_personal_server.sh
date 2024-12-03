#!/bin/bash

echo "[INFO] Generating Ramulator2 configurations and run scripts for main results"
python3 "$PWD/sim_scripts/setup_personal_server.py" \
    --ramulator_directory "$PWD" \
    --working_directory "$PWD/sim_scripts" \
    --base_config "$PWD/config/DDR5_baseline.yaml" \
    --trace_directory "$PWD/cputraces" \
    --result_directory "$PWD/results" \

echo "[INFO] Starting Ramulator2 simulations"
python3 "$PWD/sim_scripts/execute_run_script.py"