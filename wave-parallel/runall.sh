g++ -Wno-c++11-extensions waveattack_parallel.cpp -o waveattack_parallel
g++ -Wno-c++11-extensions waveattack_parallel-pro.cpp -o waveattack_parallel-pro
g++ -Wno-c++11-extensions waveattack_parallel-pro-pq.cpp -o waveattack_parallel-pro-pq

bash runscript-prac.sh
bash runscript-prac-pro.sh
bash runscript-prac-pro-nbo32-nbo64-pq.sh
