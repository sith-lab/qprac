#!/bin/bash

SLURM_PART_NAME="skylake"

echo "[INFO] Generating Ramulator2 configurations and run scripts for benign workloads"
python3 "$PWD/sim_scripts/setup_slurm.py" \
    --ramulator_directory "$PWD" \
    --working_directory "$PWD/sim_scripts" \
    --base_config "$PWD/config/DDR5_baseline.yaml" \
    --trace_directory "$PWD/cputraces" \
    --result_directory "$PWD/results" \
    --partition_name "$SLURM_PART_NAME"

echo "[INFO] Starting Ramulator2 benign simulations"
python3 "$PWD/sim_scripts/execute_run_script.py" --slurm

echo "[INFO] You can track run status with the <check_run_status.sh> script"
rm "$PWD/run.sh" 