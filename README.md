# QPRAC: Towards Secure and Practical PRAC-based Rowhammer Mitigation using Priority Queues (HPCA 2025)

## Introduction

[TODO]

## Requirements for Security Evaluations for Security Analysis

Software Dependencies: Python3 (tested on Python 3.11.5), and Python3 Package `matplotlib`.

## Steps for Generating the Security Analysis Figures

### Clone the artifact and run the code.
  - **Fetch the code:** `git clone https://github.com/sith-lab/prac.git`
  - **Run Artifact:**
    ```
      $ cd prac/security_analysis/
      $ bash ./run_artifact.sh
    ```
These commands generate the analysis results and figures for the security analysis section.

> Note: Monte Carlo simulation for R1 are not ran as they take a long time. You can do those manually
if needed by consulting the following sections.

### Script Argument Definition
  - **MIN_WAVE_LEN**          = Set of Rows to Start with (minimum)
  - **MAX_WAVE_LEN**          = Set of Rows to Start with (maximum)
  - **ABO_Delay**             = ACTs allowed after ALERT before next ALERT
  - **T_Bit**                 = T-Bit to attack
  - **NUM_QUEUE_SIZE**        = Number of queue sizes tested
  - **NUM_BIT**               = Number of t-bits tested
  - **RESULT**                = Wave equation or R1 results. Multiple results are concatenated after one another
  - **NUM_RESULTS**           = Number of results in RESULT
  - **RESULT + RESULT_PROA**  = Wave equation results, where first half is with and second half is without Proactive Mitigation

### Generating Monte Carlo Results

  - **Max R1 with or without Proactive Mitigation**
    ```
    python3 analysis_scripts/r1_equation.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_Delay> > r1.txt
    python3 analysis_scripts/r1_equation_proa.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_Delay> > r1_proa.txt
    ```
### Generating Security Analysis Results
  - **Panopticon t-bit Attack**
    ```
    python3 analysis_scripts/panopticon_attack.py <T_Bit> ... > tbit_attack.txt
    ```
  - **Maximum N_Online from equation (2)**
    ```
    python3 analysis_scripts/wave_equation.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_Delay> > wave.txt
    python3 analysis_scripts/wave_equation_proa.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_Delay> > wave_proa.txt
    ```
### Generating Figures
  - **Figure 2. Attack t-bit toggling:** 
    
    `python3 graph_scripts/figure2.py <NUM_QUEUE_SIZE> <NUM_BIT> tbit_attack.txt`
  - **Figure 6. Maximum N_Online Equation (2):** 
    
    `python3 graph_scripts/figure6.py <RESULT> <NUM_RESULTS> <MAX_WAVE_LEN>`
  - **Figure 7. Maximum R_1 from equation (3):** 
  
    `python3 graph_scripts/figure7.py r1_montecarlo/R1.txt`
  - **Figure 8. Maximum TRH:** 
  
    `python3 graph_scripts/figure8.py <RESULT> r1_montecarlo/R1.txt`
  - **Figure 11. Maximum R_1 with or without Proactive Mitigation:** 

    `python3 graph_scripts/figure11.py r1_montecarlo/R1.txt r1_montecarlo/R1_PROA.txt`
  - **Figure 12. Maximum N_Online with vs without Proactive Mitigation:**

    `python3 graph_scripts/figure12.py <RESULT + RESULT_PROA> <NUM_RESULTS> <MAX_WAVE_LEN>`
  - **Figure 13. Maximum TRH with or without Proactive Mitigation:**

    `python3 graph_scripts/figure13.py <RESULT + RESULT_PROA> r1_montecarlo/R1.txt r1_montecarlo/R1_PROA.txt`
    