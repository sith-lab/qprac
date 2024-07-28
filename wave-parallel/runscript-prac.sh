SECONDSTOTAL=0

echo "----------------- PRAC-1 ---------------------"
SECONDS=0
echo "Starting 1st Simulation"

./waveattack_parallel 1 1 1 > NBO1/NBO1-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "First process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"

SECONDS=0
echo "Starting 2nd Simulation"

./waveattack_parallel 2 1 1 > NBO2/NBO2-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Second process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 3rd Simulation"

./waveattack_parallel 4 1 1 > NBO4/NBO4-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Third process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 4th Simulation"

./waveattack_parallel 8 1 1 > NBO8/NBO8-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Fourth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 5th Simulation"

./waveattack_parallel 16 1 1 > NBO16/NBO16-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Fifth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 6th Simulation"

./waveattack_parallel 32 1 1 > NBO32/NBO32-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Sixth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 7th Simulation"

./waveattack_parallel 64 1 1 > NBO64/NBO64-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Seventh process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 8th Simulation"

./waveattack_parallel 128 1 1 > NBO128/NBO128-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Eigth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 9th Simulation"

./waveattack_parallel 256 1 1 > NBO256/NBO256-prac1.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Ninth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"

echo "----------------- PRAC-2 ---------------------"

SECONDS=0
echo "Starting 1st Simulation"

./waveattack_parallel 1 2 2 > NBO1/NBO1-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "First process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"

SECONDS=0
echo "Starting 2nd Simulation"

./waveattack_parallel 2 2 2 > NBO2/NBO2-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Second process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 3rd Simulation"

./waveattack_parallel 4 2 2 > NBO4/NBO4-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Third process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 4th Simulation"

./waveattack_parallel 8 2 2 > NBO8/NBO8-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Fourth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 5th Simulation"

./waveattack_parallel 16 2 2 > NBO16/NBO16-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Fifth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 6th Simulation"

./waveattack_parallel 32 2 2 > NBO32/NBO32-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Sixth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 7th Simulation"

./waveattack_parallel 64 2 2 > NBO64/NBO64-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Seventh process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 8th Simulation"

./waveattack_parallel 128 2 2 > NBO128/NBO128-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Eigth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 9th Simulation"

./waveattack_parallel 256 2 2 > NBO256/NBO256-prac2.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Ninth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"

echo "----------------- PRAC-4 ---------------------"

SECONDS=0
echo "Starting 1st Simulation"

./waveattack_parallel 1 4 4 > NBO1/NBO1-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "First process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"

SECONDS=0
echo "Starting 2nd Simulation"

./waveattack_parallel 2 4 4 > NBO2/NBO2-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Second process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 3rd Simulation"

./waveattack_parallel 4 4 4 > NBO4/NBO4-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Third process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 4th Simulation"

./waveattack_parallel 8 4 4 > NBO8/NBO8-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Fourth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 5th Simulation"

./waveattack_parallel 16 4 4 > NBO16/NBO16-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Fifth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 6th Simulation"

./waveattack_parallel 32 4 4 > NBO32/NBO32-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Sixth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 7th Simulation"

./waveattack_parallel 64 4 4 > NBO64/NBO64-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Seventh process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 8th Simulation"

./waveattack_parallel 128 4 4 > NBO128/NBO128-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Eigth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


SECONDS=0
echo "Starting 9th Simulation"

./waveattack_parallel 256 4 4 > NBO256/NBO256-prac4.txt

# Check if the first process completed successfully
if [ $? -ne 0 ]; then
  echo "Ninth process failed!"
  exit 1
fi

echo "Elapsed Time (using \$SECONDS): $SECONDS seconds"


echo "-- TOTAL SIM TIME (using \$SECONDS): $SECONDSTOTAL seconds --"
