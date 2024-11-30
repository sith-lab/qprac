# QPRAC: Towards Secure and Practical PRAC-based Rowhammer Mitigation using Priority Queues (HPCA 2025)

## Introduction

[TODO]

## Requirements for Security Evaluations for Security Analysis

- **Software Dependencies:** Python3 (Tested on V3.11.5), Python3 Package `matplotlib`.

## Steps for Generating the Security Analysis Figures

### Clone the artifact and run the code.
  - **Fetch the code:** `git clone https://github.com/sith-lab/prac.git`
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
These commands generate the analysis results and figures for the security analysis section.

> **Note: Regenerating the data will take around <> hours.**

### Script Argument Definition List
  - **MIN_WAVE_LEN**          = Set of Rows to Start with (minimum)
  - **MAX_WAVE_LEN**          = Set of Rows to Start with (maximum)
  - **T_Bit**                 = T-Bit to attack
  - **TESTED_BITS**           = Number of t-bits tested
  - **RESULT_EQ2/EQ2_PRO/EQ3/EQ3_PRO**                = Equation result file name, where results from different PRAC configurations are concatenated from 1-4.

### Generating Monte Carlo Results

  - **Max R1 with or without Proactive Mitigation**
    ```bash
      $ cd qprac/security_analysis/analysis_scripts
      $ python3 equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 equation3_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3_PRO>
    ```
### Generating Security Analysis Results
  - **Panopticon t-bit Attack**
    ```bash
      $ cd qprac/security_analysis/analysis_scripts
      $ python3 tbit_attack.py <T_Bit> ... > tbit_attack.txt
    ```
  - **Maximum N_Online from equation (2)**
    ```
      $ cd qprac/security_analysis/analysis_scripts
      $ python3 equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 equation2_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2_PRO>
    ```
### Generating Figures
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
      $ #   python3 ../analysis_scripts/equation2.py 0 $((2**17)) >> PRAC1-4.txt
      $ #   python3 figure6_plot.py PRAC1-4.txt $((2**17))
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 figure6.py <RESULT_EQ2> <MAX_WAVE_LEN>
    ```
  - **Figure 7. Maximum R_1 from equation (3):** 

    ```bash
      $ cd qprac/security_analysis/figure7
      $ # Example: 
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) > R1.txt
      $ #   python3 figure7_plot.py R1.txt
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 figure7_plot.py <RESULT_EQ3>
    ```
  - **Figure 8. Maximum TRH:** 

    ```bash
      $ cd qprac/security_analysis/figure8
      $ # Example:
      $ #   python3 ../analysis_scripts/equation2.py 0 $((2**17)) >> PRAC1-4.txt
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) > R1.txt
      $ #   python3 figure8_plot.py PRAC1-4.txt R1.txt
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 figure8.py <RESULT_EQ2> <RESULT_EQ3>
    ```
  - **Figure 11. Maximum R_1 with or without Proactive Mitigation:** 

    ```bash
      $ cd qprac/security_analysis/figure11
      $ # Example:
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) > R1.txt
      $ #   python3 ../analysis_scripts/equation3_pro.py 0 $((2**17)) > R1_PRO.txt
      $ #   python3 figure8_plot.py PRAC1-4.txt R1.txt
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 ../analysis_scripts/equation3_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3_PRO>
      $ python3 figure11_plot.py <RESULT_EQ3> <RESULT_EQ3_PRO>
    ```
  - **Figure 12. Maximum N_Online with vs without Proactive Mitigation:**

    ```bash
      $ cd qprac/security_analysis/figure12
      $ # Example:
      $ #   python3 ../analysis_scripts/equation3.py 0 $((2**17)) > R1.txt
      $ #   python3 ../analysis_scripts/equation3_pro.py 0 $((2**17)) > R1_PRO.txt
      $ #   python3 figure8_plot.py PRAC1-4.txt R1.txt
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 ../analysis_scripts/equation2_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2_PRO>
      $ python3 figure12.py <RESULT_EQ2> <RESULT_EQ2_PRO> <MAX_WAVE_LEN>
    ```
  - **Figure 13. Maximum TRH with or without Proactive Mitigation:**

    ```bash
      $ cd qprac/security_analysis/figure13
      $ # Example:
      $ # python3 ../analysis_scripts/equation2.py 0 $((2**17)) > PRAC1-4.txt
      $ # python3 ../analysis_scripts/equation2_pro.py 0 $((2**17)) > PRAC1-4_PRO.txt
      $ # python3 ../analysis_scripts/equation3.py 0 $((2**17)) > R1.txt
      $ # python3 ../analysis_scripts/equation3_pro.py 0 $((2**17)) > R1_PRO.txt
      $ # python3 figure13_plot.py PRAC1-4.txt PRAC1-4_PRO.txt R1.txt R1_PRO.txt
      $ python3 ../analysis_scripts/equation2.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2>
      $ python3 ../analysis_scripts/equation2_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> > <RESULT_EQ2_PRO>
      $ python3 ../analysis_scripts/equation3.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3>
      $ python3 ../analysis_scripts/equation3_pro.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <RESULT_EQ3_PRO>
      $ python3 figure13.py <RESULT_EQ2> <RESULT_EQ2_PRO> <RESULT_EQ3> <RESULT_EQ3_PRO>
    ```
