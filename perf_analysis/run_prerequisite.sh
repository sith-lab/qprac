#!/bin/bash
## 1. Install python dependences
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 1. Installing Python dependencies"
echo "#####################"
pip3 install -r python_dependencies.txt

## 2. Download the required traces
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 2. Downloading Required Traces"
echo "#####################"
# Create the cputraces directory if it doesn't exist
mkdir -p cputraces
if [ "$(ls -A cputraces/)" ]; then
  echo "cputraces directory already contains the traces. Skipping download"
else
  echo "cputraces directory is empty"
  echo "Downloading the required traces into the cputraces directory"
  python3 ./download_traces.py
  echo "Decompressing the traces into the cputraces directory"
  tar -xzvf cputraces.tar.gz --no-same-owner -C cputraces/
fi

## 3. Build Ramulator2
echo "---------------------------"
echo ""
echo "#####################"
echo "[INFO] 3. Building Ramulator2"
echo "#####################"
rm -rf ./build/
bash "$PWD/build.sh"