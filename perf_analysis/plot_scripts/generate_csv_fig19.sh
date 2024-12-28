#!/bin/bash

# Input and output files
INPUT_FILE="fig19.out"
OUTPUT_FILE="../results/csvs/fig19.csv"

python3 bw_degradation_fig19.py > "$INPUT_FILE"


# Headers for the CSV file
echo "NBO,QPRAC-RFMab,QPRAC-RFMab+Proactive (default),QPRAC-RFMsb+Proactive,QPRAC-RFMpb+Proactive" > "$OUTPUT_FILE"

# NBO values
nbos=("16" "32" "64" "128")

# Read data from the input file into an array
mapfile -t data < "$INPUT_FILE"

# Write data to the CSV file
for i in "${!nbos[@]}"; do
    echo "${nbos[$i]},${data[$i]},${data[$i+4]},${data[$i+8]},${data[$i+12]}" >> "$OUTPUT_FILE"
done

echo "CSV file '$OUTPUT_FILE' has been generated successfully."
