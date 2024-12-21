#!/bin/bash

### Manually set SLURM variables here (if not passed as environment variables)
SLURM_PART_NAME="${SLURM_PART_NAME:-skylake}"  # Default value is "skylake" if not set
SLURM_PART_DEF_MEM="${SLURM_PART_DEF_MEM:-4G}"  # Default memory size is '4G' if not set
SLRUM_PART_BIG_MEM="${SLRUM_PART_BIG_MEM:-12G}"  # Default memory size is '12G' if not set

# Export MAX_SLURM_JOBS with default values if not already set
export MAX_SLURM_JOBS=${MAX_SLURM_JOBS:-500}

# Check if SLURM variables are set (if manually overridden or passed from environment)
echo "[INFO] SLURM_PART_NAME: $SLURM_PART_NAME"
echo "[INFO] SLURM_PART_DEF_MEM: $SLURM_PART_DEF_MEM"
echo "[INFO] SLRUM_PART_BIG_MEM: $SLRUM_PART_BIG_MEM"

echo "[INFO] Generating simulation configurations and run scripts for Figure 20 using Slurm"
python3 "$PWD/sim_scripts/setup_slurm_fig20.py" \
    --ramulator_directory "$PWD" \
    --working_directory "$PWD/sim_scripts" \
    --base_config "$PWD/config/DDR5_baseline.yaml" \
    --trace_directory "$PWD/cputraces" \
    --result_directory "$PWD/results" \
    --partition_name "$SLURM_PART_NAME" \
    --partition_default_memory "$SLURM_PART_DEF_MEM" \
    --partition_big_memory "$SLRUM_PART_BIG_MEM"

echo "[INFO] Starting simulations for Figure 20"
python3 "$PWD/sim_scripts/execute_run_script_fig20.py" --slurm

echo "[INFO] Fired all simulations for Figure 20, this can take 1.5+ days to complete."
rm "$PWD/run.sh" 