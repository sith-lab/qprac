#!/bin/bash

# Zenodo download link
url="https://zenodo.org/record/14607144/files/QPRAC_HPCA25_ramulator2_traces.tar.gz?download=1"

# Specify the output filename
output_file="cputraces.tar.gz"

# Download the file using wget
wget -O "$output_file" "$url"
