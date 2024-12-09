#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 --method <slurm|personal> --artifact <all|main>"
    echo "
Options:"
    echo "  --method <slurm|personal>    Specify the execution method"
    echo "  --artifact <all|main>        Specify whether to run all artifacts or just main results"
    exit 1
}

# Initialize variables
METHOD=""
ARTIFACT=""

#### Run configuration settings
PERSONAL_RUN_THREADS=80 # Set Maximum concurrent threads here
#### Set Here if you use SLURM
# SLURM_PART_NAME=""
SLURM_PART_NAME="skylake"
SLURM_PART_DEF_MEM='4G' 
SLRUM_PART_BIG_MEM='12G'
MAX_SLURM_JOBS=1000    # Set Maximum slurm jobs here

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --method)
            METHOD="$2"
            shift 2
            ;;
        --artifact)
            ARTIFACT="$2"
            shift 2
            ;;
        *)
            echo "[ERROR] Unknown option: $1"
            usage
            ;;
    esac
done

# Validate required arguments
if [[ -z "$METHOD" ]]; then
    echo "[ERROR] --method is required"
    usage
fi

if [[ -z "$ARTIFACT" ]]; then
    echo "[ERROR] --artifact is required"
    usage
fi

## 1. Install python dependences
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 1. Installing Python dependencies"
echo "#####################"
pip3 install -r python_dependencies.txt

## 2. Download the required traces
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 2. Downloading Required Traces"
echo "#####################"
# Create the cputraces directory if it doesn't exist
mkdir -p cputraces
if [ "$(ls -A cputraces/)" ]; then
  echo "cputraces directory already contains the traces. Skipping download"
else
  echo "cputraces directory is empty"
  echo "Downloading the required traces into the cputraces directory"
  python3 ./download_traces.py
  echo "Decompressing the traces into the cputraces directory"
  tar -xzvf cputraces.tar.gz --no-same-owner -C cputraces/
fi

## 3. Build Ramulator2
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 3. Building Ramulator2"
echo "#####################"
rm -rf ./build/
bash "$PWD/build.sh"

## 4. Run Ramulator2 for the main results only (Figure 14 and 15)
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 4. Running Artifact"
echo "#####################"
# Set MAX_SLURM_JOBS and PERSONAL_RUN_THREADS as environment variables
export MAX_SLURM_JOBS=$MAX_SLURM_JOBS
export PERSONAL_RUN_THREADS=$PERSONAL_RUN_THREADS

# Execute based on method and artifact choice
if [[ "$METHOD" == "slurm" ]]; then
    echo "[INFO] Running experiments with SLURM"
    if [[ "$ARTIFACT" == "all" ]]; then
        echo "[INFO] Running all required experiments"
        echo "[INFO] Running experiments for Figure 14 and 15"
        SLURM_PART_NAME="$SLURM_PART_NAME" SLURM_PART_DEF_MEM="$SLURM_PART_DEF_MEM" SLRUM_PART_BIG_MEM="$SLRUM_PART_BIG_MEM" bash "$PWD/run_slurm_fig14_15.sh"
        echo "[INFO] Running experiments for Figure 16"
        SLURM_PART_NAME="$SLURM_PART_NAME" SLURM_PART_DEF_MEM="$SLURM_PART_DEF_MEM" SLRUM_PART_BIG_MEM="$SLRUM_PART_BIG_MEM" bash "$PWD/run_slurm_fig16.sh"
        echo "[INFO] Running experiments for Figure 17"
        SLURM_PART_NAME="$SLURM_PART_NAME" SLURM_PART_DEF_MEM="$SLURM_PART_DEF_MEM" SLRUM_PART_BIG_MEM="$SLRUM_PART_BIG_MEM" bash "$PWD/run_slurm_fig17.sh"
        echo "[INFO] Running experiments for Figure 18"
        SLURM_PART_NAME="$SLURM_PART_NAME" SLURM_PART_DEF_MEM="$SLURM_PART_DEF_MEM" SLRUM_PART_BIG_MEM="$SLRUM_PART_BIG_MEM" bash "$PWD/run_slurm_fig18.sh"
    elif [[ "$ARTIFACT" == "main" ]]; then
        echo "[INFO] Running main experiments (Figure 14 and 15)"
        SLURM_PART_NAME="$SLURM_PART_NAME" SLURM_PART_DEF_MEM="$SLURM_PART_DEF_MEM" SLRUM_PART_BIG_MEM="$SLRUM_PART_BIG_MEM" bash "$PWD/run_slurm_fig14_15.sh"
    else
        echo "[ERROR] Invalid artifact choice: $ARTIFACT"
        usage
    fi

elif [[ "$METHOD" == "personal" ]]; then
    echo "[INFO] Running experiments on personal server"
    if [[ "$ARTIFACT" == "all" ]]; then
        echo "[INFO] We highly recommend running the main experiments and reviewing the results first before proceeding with all experiments if using a personal server. Running all experiments on a personal server with limited resources (e.g., < 256GB DRAM and < 40 cores) can take a significant amount of time, potentially taking up to a week."
        echo "[INFO] Running experiments for Figure 14 and 15"
        bash "$PWD/run_ps_fig14_15.sh"
        bash "$PWD/run_ps_except_main_results.sh"
    elif [[ "$ARTIFACT" == "main" ]]; then
        echo "[INFO] Running main experiments (Figure 14 and 15)"
        bash "$PWD/run_ps_fig14_15.sh"
    else
        echo "[ERROR] Invalid artifact choice: $ARTIFACT"
        usage
    fi

else
    echo "[ERROR] Invalid method: $METHOD"
    usage
fi