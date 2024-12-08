## QPRAC (HPCA 2025)

### Introduction

This is the code artifact for the paper 
"QPRAC: Secure and Practical PRAC-based Rowhammer Mitigation using Priority Queues", whick will appear in [HPCA 2025](https://hpca-conf.org/2025/). 

Authors: Jeonghyun Woo (University of British Columbia), Shaopeng (Chris) Lin (University of Toronto), Prashant J. Nair (University of British Columbia), Aamer Jaleel (NVIDIA), Gururaj Saileshwar (University of Toronto).

You can reproduce our security and performance evaluations as follows.

### Acknowledgement   
 This artifact and simulation infrastructure have been adapted from [SRS (HPCA 2023)](https://github.com/STAR-Laboratory/scale-srs) and [BreakHammer (MICRO 2024)](https://github.com/CMU-SAFARI/BreakHammer).

# Security Analysis
### Requirements

**Security Evaluations:**
- Python3 (Tested on V3.11.5)
- Python3 Package `matplotlib` for plotting
  
### Steps for Security Evaluations

Please run the following steps to regenerate the security analysis and figures:

### Clone the artifact and run the code.
  - **Fetch the code:** `git clone https://github.com/sith-lab/qprac.git`
  - **Run Artifact:**
    ```
      $ cd qprac/security_analysis
      $ bash ./run_artifact.sh
    ```
  - **Run Artifact without regenerating data**
    ```
      $ cd qprac/security_analysis
      $ bash ./run_artifact.sh --use-sample
    ```
  - **Run Artifact with regeneration of data (monte-carlo analysis) (slower - 2 hours):**
    ```
      $ cd qprac/security_analysis
      $ bash ./run_artifact.sh
    ```
These scripts execute the following commands outlined below.

#### Steps Run By Script
Below are the steps run by our above script in an automated manner. 
  - **Monte Carlo Analysis (for Max R1):**
    This obtains the Max R1 value without and with Proactive Mitigation, used for Fig-7 and Fig-11 respectively.
    ```bash
      $ cd qprac/security_analysis/analysis_scripts
      $ python3 equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 equation3_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3_PRO>
    ```
  - **Figure 2. Attack t-bit toggling:** 
    
    ```bash
      $ cd qprac/security_analysis/figure2
      $ # Example: 
      $ #   python3 ../analysis_scripts/tbit_attack.py 6 8 10 > tbit_attack.txt
      $ #   python3 figure2_plot.py 3 tbit_attack.txt
      $ python3 ../analysis_scripts/tbit_attack.py <T_Bit> ... > tbit_attack.txt
      $ python3 figure2.py <TESTED_BITS> tbit_attack.txt
    ```
  - **Figure 6. Maximum N_Online Equation (2):** 
    
    ```bash
      $ cd qprac/security_analysis/figure6
      $ # Example: 
      $ #   python3 ../analysis_scripts/equation2.py 0 $((2**17)) > PRAC1-4.txt
      $ #   python3 figure6_plot.py PRAC1-4.txt $((2**17))
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 figure6.py <RESULT_EQ2> <MAX_WAVE_LEN>
    ```
  - **Figure 7. Maximum R_1 from equation (3):** 

    ```bash
      $ cd qprac/security_analysis/figure7
      $ # Example: 
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) R1.txt
      $ #   python3 figure7_plot.py R1.txt
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 figure7_plot.py <RESULT_EQ3>
    ```
  - **Figure 8. Maximum TRH:** 

    ```bash
      $ cd qprac/security_analysis/figure8
      $ # Example:
      $ #   python3 ../analysis_scripts/equation2.py 0 $((2**17)) > PRAC1-4.txt
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) R1.txt
      $ #   python3 figure8_plot.py PRAC1-4.txt R1.txt
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 figure8.py <RESULT_EQ2> <RESULT_EQ3>
    ```
  - **Figure 11. Maximum R_1 with or without Proactive Mitigation:** 

    ```bash
      $ cd qprac/security_analysis/figure11
      $ # Example:
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) R1.txt
      $ #   python3 ../analysis_scripts/equation3_pro.py 0 $((2**17)) R1_PRO.txt
      $ #   python3 figure11_plot.py R1.txt R1_PRO.txt
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 ../analysis_scripts/equation3_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3_PRO>
      $ python3 figure11_plot.py <RESULT_EQ3> <RESULT_EQ3_PRO>
    ```
  - **Figure 12. Maximum N_Online with vs without Proactive Mitigation:**

    ```bash
      $ cd qprac/security_analysis/figure12
      $ # Example:
      $ #   python3 ../analysis_scripts/equation2.py 0 $((2**17)) > PRAC1-4.txt
      $ #   python3 ../analysis_scripts/equation2_pro.py 0 $((2**17)) > PRAC1-4_PRO.txt
      $ #   python3 figure12_plot.py PRAC1-4.txt PRAC1-4_PRO.txt $((2**17))
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 ../analysis_scripts/equation2_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2_PRO>
      $ python3 figure12.py <RESULT_EQ2> <RESULT_EQ2_PRO> <MAX_WAVE_LEN>
    ```
  - **Figure 13. Maximum TRH with or without Proactive Mitigation:**

    ```bash
      $ cd qprac/security_analysis/figure13
      $ # Example:
      $ #   python3 ../analysis_scripts/equation2.py 0 $((2**17)) > PRAC1-4.txt
      $ #   python3 ../analysis_scripts/equation2_pro.py 0 $((2**17)) > PRAC1-4_PRO.txt
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) R1.txt
      $ #   python3 ../analysis_scripts/equation3_pro.py 0 $((2**17)) R1_PRO.txt
      $ #   python3 figure13_plot.py PRAC1-4.txt PRAC1-4_PRO.txt R1.txt R1_PRO.txt
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 ../analysis_scripts/equation2_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2_PRO>
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 ../analysis_scripts/equation3_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3_PRO>
      $ python3 figure13.py <RESULT_EQ2> <RESULT_EQ2_PRO> <RESULT_EQ3> <RESULT_EQ3_PRO>
    ```

# Performance Evaluations Using Ramulator2

## Requirements
### Software Dependencies
- **g++** with C++20 support (tested with version 12.4.0).
- **Python3** (recommended: version 3.10 or above).

### Hardware Dependencies
- **Personal Server**: A CPU with at least 128GB of memory and 64+ cores is recommended to run all benchmarks efficiently.

---

## Steps for Performance Evaluations

### 1. Clone the Repository
Ensure you have already cloned the repository during the security analysis:
```bash
git clone https://github.com/sith-lab/qprac.git
```

### 2. Set Simulation Configuration Parameters

#### Using SLURM
Configure the following parameters in `./perf_analysis/run_artifact.sh` or relevant SLURM scripts (`run_slurm_fig*.sh`):
- **`SLURM_PART_NAME`**: Partition name for SLURM jobs.
- **`SLURM_PART_DEF_MEM`**: Default memory size for jobs (recommended: ≥4GB).
- **`SLURM_PART_BIG_MEM`**: Memory size for jobs requiring large memory (recommended: ≥12GB).
- **`MAX_SLURM_JOBS`**: Maximum number of SLURM jobs submitted.

#### Using a Personal Server
Configure the following parameter in `./perf_analysis/run_artifact.sh` or `run_ps_fig*.sh`:
- **`PERSONAL_RUN_THREADS`**: Number of parallel threads to use for simulations.

### 3. Run the Artifact
Run the following commands to install dependencies, build Ramulator2, and execute simulations.

#### Main Experiments Only (Figures 14 and 15)
- **Using SLURM**:
  ```bash
  cd perf_analysis/
  bash ./run_artifact.sh --method slurm --artifact main
  ```
- **Using a Personal Server**:
  ```bash
  cd perf_analysis/
  bash ./run_artifact.sh --method personal --artifact main
  ```

#### All Experiments (Figures 14–18)
- **Using SLURM**:
  ```bash
  cd perf_analysis/
  bash ./run_artifact.sh --method slurm --artifact all
  ```
- **Using a Personal Server**:
  Running all experiments on a personal server may take significant time (days to a week). No single script is provided; follow manual steps for individual experiments.

### 4. Generate Figures
After completing simulations, use the commands below to generate plots. Alternatively, use the Jupyter Notebook (`perf_analysis/plot_scripts/plot.ipynb`). Generated PDFs can be found in `perf_analysis/results/plots/`.

#### Main Figures (Figures 14 and 15)
```bash
cd perf_analysis/
bash ./plot_main_figures.sh
```

#### All Figures (Figures 14–18)
```bash
cd perf_analysis/
bash ./plot_main_figures.sh
```

---

## Detailed Steps

### Prerequisites
Install Python dependencies, download required traces, and build Ramulator2:
   ```bash
   cd perf_analysis/
   bash run_prerequisite.sh
   ```

### Execution
Set simulation configuration parameters:
- **SLURM**: Configure `SLURM_PART_NAME`, `SLURM_PART_DEF_MEM`, `SLURM_PART_BIG_MEM`, and `MAX_SLURM_JOBS` in `run_slurm_fig*.sh`.
- **Personal Server**: Configure `PERSONAL_RUN_THREADS` in `run_ps_fig*.sh`.

### Run experiments:

#### Using SLURM
- **Main Results (Figures 14 and 15)**:
  ```bash
  cd perf_analysis/
  bash run_slurm_fig14_15.sh
  ```
- **Figure 16: Sensitivity to Number of RFMs per Alert**:
  ```bash
  cd perf_analysis/
  bash run_slurm_fig16.sh
  ```
- **Figure 17: Sensitivity to Service Queue Size**:
  ```bash
  cd perf_analysis/
  bash run_slurm_fig17.sh
  ```
- **Figure 18: Sensitivity to Back-Off Threshold**:
  ```bash
  cd perf_analysis/
  bash run_slurm_fig18.sh
  ```

#### Using a Personal Server
- **Main Results (Figures 14 and 15)**:
  ```bash
  cd perf_analysis/
  bash run_ps_fig14_15.sh
  ```
- **Figure 16: Sensitivity to Number of RFMs per Alert**:
  ```bash
  cd perf_analysis/
  bash run_ps_fig16.sh
  ```
- **Figure 17: Sensitivity to Service Queue Size**:
  ```bash
  cd perf_analysis/
  bash run_ps_fig17.sh
  ```
- **Figure 18: Sensitivity to Back-Off Threshold**:
  ```bash
  cd perf_analysis/
  bash run_ps_fig18.sh
  ```

### Collate Results
Once simulations complete, generate CSV files using the commands below. Generated csv files can be found in `perf_analysis/results/csvs/`.
- **Main Results (Figures 14 and 15)**:
  ```bash
  cd perf_analysis/plot_scripts
  python3 generate_csv_fig14_15.py
  ```
- **Figure 16**:
  ```bash
  python3 generate_csv_fig16.py
  ```
- **Figure 17**:
  ```bash
  python3 generate_csv_fig17.py
  ```
- **Figure 18**:
  ```bash
  python3 generate_csv_fig18.py
  ```

### Generate Plots
After collating results, generate the plots in using the commands below. Alternatively, use the Jupyter Notebook (`perf_analysis/plot_scripts/plot.ipynb`). Generated PDFs can be found in `perf_analysis/results/plots/`.
- **Main Results (Figures 14 and 15)**:
  ```bash
  cd perf_analysis/plot_scripts
  python3 plot_fig14_15.py
  ```
- **Figure 16**:
  ```bash
  python3 plot_fig16.py
  ```
- **Figure 17**:
  ```bash
  python3 plot_fig17.py
  ```
- **Figure 18**:
  ```bash
  python3 plot_fig18.py
  ```