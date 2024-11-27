#!/bin/bash

echo "Note: Figures generated are stored in output/graphs."
echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 2. Attack t-bit toggling"
echo "#####################"
echo ""
python3 analysis_scripts/panopticon_attack.py 6 8 10 > temp.txt
python3 graph_scripts/graph_panop_multi.py 13 3 temp.txt
rm temp.txt

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 6. Maximum N_Online from equation (2)"
echo "#####################"
echo ""
# python3 analysis_scripts/wave_equation.py <MIN_R1> <MAX_R1> <PRAC-N>
python3 analysis_scripts/wave_equation.py 0 $((1 << 17)) 1 > PRAC1-4.txt
python3 analysis_scripts/wave_equation.py 0 $((1 << 17)) 2 >> PRAC1-4.txt
python3 analysis_scripts/wave_equation.py 0 $((1 << 17)) 4 >> PRAC1-4.txt
python3 graph_scripts/prac_nonline.py PRAC1-4.txt 3 $((1 << 17))

echo "Note: R1 Generation is very slow and this script uses pre-generated data." 
echo "Please use the commented-out script for real generation if needed"
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 7. Maximum R_1 from equation (3)"
echo "#####################"
echo ""
# python3 analysis_scripts/r1_equation.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_ACT> <ABO_Delay> <N_BO>
python3 graph_scripts/r1.py SetupPhaseData/R1.txt

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 8. Maximum TRH"
echo "#####################"
echo ""
python3 graph_scripts/trh.py PRAC1-4.txt SetupPhaseData/R1.txt

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 11. Maximum R_1 with or without Proactive Mitigation."
echo "#####################"
echo ""
python3 graph_scripts/r1_proa.py SetupPhaseData/R1.txt SetupPhaseData/R1_PROA.txt 

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 12. Maximum N_Online for PRAC with vs PRAC without Proactive Mitigation"
echo "#####################"
echo ""
python3 analysis_scripts/wave_equation_proa.py 0 $((1 << 17)) 1 >> PRAC1-4.txt
python3 analysis_scripts/wave_equation_proa.py 0 $((1 << 17)) 2 >> PRAC1-4.txt
python3 analysis_scripts/wave_equation_proa.py 0 $((1 << 17)) 4 >> PRAC1-4.txt
python3 graph_scripts/prac_nonline_proa.py PRAC1-4.txt 6 $((1 << 17))

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 13. Maximum TRH with or without Proactive Mitigation"
echo "#####################"
echo ""
python3 graph_scripts/trh_proa.py PRAC1-4.txt SetupPhaseData/R1.txt SetupPhaseData/R1_PROA.txt

rm PRAC1-4.txt
echo "Figure Generation completed!."