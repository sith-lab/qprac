#!/bin/bash

echo "Note: Figures generated are stored in output/graphs."
echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 2. Attack t-bit toggling"
echo "#####################"
echo ""
python3 analysis_scripts/tbit_attack.py 6 8 10 > tbit_attack.txt
python3 graph_scripts/figure2.py 13 3 tbit_attack.txt

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 6. Maximum N_Online from equation (2)"
echo "#####################"
echo ""
# python3 analysis_scripts/wave_equation.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_Delay>
python3 analysis_scripts/wave_equation.py 0 $((1 << 17)) 1 > PRAC1-4.txt
python3 analysis_scripts/wave_equation.py 0 $((1 << 17)) 2 >> PRAC1-4.txt
python3 analysis_scripts/wave_equation.py 0 $((1 << 17)) 4 >> PRAC1-4.txt
python3 graph_scripts/figure6.py PRAC1-4.txt 3 $((1 << 17))

echo "Note: R1 Generation is very slow and this script uses pre-generated data." 
echo "Please use the commented-out script for real generation if needed"
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 7. Maximum R_1 from equation (3)"
echo "#####################"
echo ""
# python3 analysis_scripts/r1_equation.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_Delay>
python3 graph_scripts/figure7.py graph_scripts/r1_montecarlo/R1.txt

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 8. Maximum TRH"
echo "#####################"
echo ""
python3 graph_scripts/figure8.py PRAC1-4.txt graph_scripts/r1_montecarlo/R1.txt

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 11. Maximum R_1 with or without Proactive Mitigation."
echo "#####################"
echo ""
python3 graph_scripts/figure11.py graph_scripts/r1_montecarlo/R1.txt graph_scripts/r1_montecarlo/R1_PROA.txt 

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 12. Maximum N_Online with vs without Proactive Mitigation"
echo "#####################"
echo ""
python3 analysis_scripts/wave_equation_proa.py 0 $((1 << 17)) 1 >> PRAC1-4.txt
python3 analysis_scripts/wave_equation_proa.py 0 $((1 << 17)) 2 >> PRAC1-4.txt
python3 analysis_scripts/wave_equation_proa.py 0 $((1 << 17)) 4 >> PRAC1-4.txt
python3 graph_scripts/figure12.py PRAC1-4.txt 6 $((1 << 17))

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 13. Maximum TRH with or without Proactive Mitigation"
echo "#####################"
echo ""
python3 graph_scripts/figure13.py PRAC1-4.txt graph_scripts/r1_montecarlo/R1.txt graph_scripts/r1_montecarlo/R1_PROA.txt

echo "Figure Generation completed!."