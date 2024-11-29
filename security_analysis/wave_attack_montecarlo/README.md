## Requirements for Wave Attack Monte Carlo Simulation

- **Software Dependencies:** C++11 (Successfully compiles on g++ versions: 9.4.0 & 13.1.0) and Linux Package `gnuplot`.

- **Data Dependencies:** Monte Carlo Simulation for the Wave Attack on PRAC depends on data in `wave-parrallel/NBO*` due to long run time.

## Steps for Generating the Wave Attack Monte Carlo Simulation

### Clone the artifact and run the code.
- **Fetch the code:** `git clone https://github.com/sith-lab/prac.git`
  - **Run Artifact:**
    ```
      $ cd qprac/security_analysis/wave_attack_montecarlo
      $ bash ./runall.sh
      $ bash ./make_plots.sh
    ```
  - **Clear Data & Plots**
    ```
      $ bash clean_data.sh
      $ bash clean_plots.sh
    ```
> Note: the graphs and data have already been provided in the repository. The above scripts will

These commands run all the following steps (compile, execute, and generate a visual plot for the output results). You may also follow these steps manually.

### Compile
Compile the Monte Carlo Simulation of wave attack on PRAC:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ g++ -Wno-c++11-extensions waveattack_parallel.cpp -o waveattack_parallel
```

Compile the Monte Carlo Simulation of wave attack with proactive mitigation on PRAC:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ g++ -Wno-c++11-extensions waveattack_parallel-pro.cpp -o waveattack_parallel-pro
```

Compile the Monte Carlo Simulation of wave attack with proactive mitigation on QPRAC:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ g++ -Wno-c++11-extensions waveattack_parallel-pro-pq.cpp -o waveattack_parallel-pro-pq
```

### Execute

Run the wave attack on PRAC:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ bash runscript-prac.sh
```

Run the wave attack with proactive mitigation on PRAC:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ bash runscript-prac-pro.sh
```

Run the wave attack with proactive mitigation on QPRAC:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ bash runscript-prac-pro-nbo32-nbo64-pq.sh
```

### Generate Plots

Generate the pdf files of the Monte Carlo Simulations using the following commands:
```
  $ cd qprac/security_analysis/wave_attack_montecarlo
  $ bash ./make_plots.sh
```