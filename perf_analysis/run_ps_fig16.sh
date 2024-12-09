#!/bin/bash
# Export PERSONAL_RUN_THREADS with default values if not already set
export PERSONAL_RUN_THREADS=${PERSONAL_RUN_THREADS:-40}

echo "[INFO] Generating simulation configurations and run scripts for Figure 16 Using Personal Server"
python3 "$PWD/sim_scripts/setup_ps_fig16.py" \
    --ramulator_directory "$PWD" \
    --working_directory "$PWD/sim_scripts" \
    --base_config "$PWD/config/DDR5_baseline.yaml" \
    --trace_directory "$PWD/cputraces" \
    --result_directory "$PWD/results" \

echo "[INFO] Starting simulations for Figure 16"
python3 "$PWD/sim_scripts/execute_run_script_fig16.py"