#!/bin/bash

# Default values (optional)
use_sample=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --use-sample)
      use_sample=true
      shift
      ;;
    *)
      echo "Usage: $0 [--use-sample]"
      exit 1
      ;;
  esac
done

# Use the argument
if [ "$use_sample" = true ]; then
  echo "Using sample data."
else
  echo "Not using sample data. Regenerating data required."
    echo ""
    echo "---------------------------"
    echo ""
    echo "#####################"
    echo "Generating Results needed for Artifacts..."
    echo "#####################"
    echo ""
    echo "Note: This can take around <> hours. If you do not want to run the entire data, add '--use-sample' option to use the existing sample data instead."
    python3 analysis_scripts/tbit_attack.py 6 8 10 > tbit_attack.txt
    python3 analysis_scripts/equation2.py 0 $((2**17)) > PRAC1-4.txt
    python3 analysis_scripts/equation2_pro.py 0 $((2**17)) > PRAC1-4_PRO.txt
    python3 analysis_scripts/equation3.py 0 $((2**17)) R1.txt &
    python3 analysis_scripts/equation3_pro.py 0 $((2**17)) R1_PRO.txt &
    wait
fi

echo "Note: Figures generated are stored in figure*/ as figure*.pdf."
echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 2. Attack t-bit toggling"
echo "#####################"
echo ""
cd figure2
if [ "$use_sample" = true ]; then
    python3 figure2_plot.py 3 sample_data/tbit_attack.txt
else
    python3 figure2_plot.py 3 ../tbit_attack.txt
fi
cd ..

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 6. Maximum N_Online from equation (2)"
echo "#####################"
echo ""
cd figure6
if [ "$use_sample" = true ]; then
    python3 figure6_plot.py sample_data/PRAC1-4.txt $((2**17))
else
    python3 figure6_plot.py ../PRAC1-4.txt $((2**17))
fi
cd ..

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 7. Maximum R_1 from equation (3)"
echo "#####################"
echo ""
cd figure7
if [ "$use_sample" = true ]; then
    python3 figure7_plot.py sample_data/R1.txt
else
    python3 figure7_plot.py ../R1.txt
fi
cd ..

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 8. Maximum TRH"
echo "#####################"
echo ""
cd figure8
if [ "$use_sample" = true ]; then
    python3 figure8_plot.py sample_data/PRAC1-4.txt sample_data/R1.txt
else
    python3 figure8_plot.py ../PRAC1-4.txt ../R1.txt
fi
cd ..

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 11. Maximum R_1 with or without Proactive Mitigation."
echo "#####################"
echo ""
cd figure11
if [ "$use_sample" = true ]; then
    python3 figure11_plot.py sample_data/R1.txt sample_data/R1_PRO.txt
else
    python3 figure11_plot.py ../R1.txt ../R1_PRO.txt
fi
cd ..


echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 12. Maximum N_Online with vs without Proactive Mitigation"
echo "#####################"
echo ""
cd figure12
if [ "$use_sample" = true ]; then
    python3 figure12_plot.py sample_data/PRAC1-4.txt sample_data/PRAC1-4_PRO.txt $((2**17))
else
    python3 figure12_plot.py ../PRAC1-4.txt ../PRAC1-4_PRO.txt $((2**17))
fi
cd ..

echo ""
echo "---------------------------"
echo ""
echo "#####################"
echo "Figure 13. Maximum TRH with or without Proactive Mitigation"
echo "#####################"
echo ""
cd figure13
if [ "$use_sample" = true ]; then
    python3 figure13_plot.py sample_data/PRAC1-4.txt sample_data/PRAC1-4_PRO.txt sample_data/R1.txt sample_data/R1_PRO.txt
else
    python3 figure13_plot.py ../PRAC1-4.txt ../PRAC1-4_PRO.txt ../R1.txt ../R1_PRO.txt
fi
cd ..

echo "Figure Generation completed!."