## QPRAC (HPCA 2025)

### Introduction

This is the code artifact for the paper 
"QPRAC: Secure and Practical PRAC-based Rowhammer Mitigation using Priority Queues" Published in HPCA 2025. 
Jeonghyun Woo, Shaopeng (Chris) Lin, Prashant J. Nair, Aamer Jaleel, Gururaj Saileshwar.

You can reproduce our security and performance evaluations as follows.

### Requirements

**Security Evaluations:**
- Python3 (Tested on V3.11.5)
- Python3 Package `matplotlib` for plotting

**Performance Evaluations:**
- [TODO]
  
### Steps for Security Evaluations

Please run the following steps to regenerate the security analysis and figures:

  - **Fetch the code:** `git clone https://github.com/sith-lab/prac.git`
  - **Run Artifact without regenerating data (faster - few minutes)** 
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
