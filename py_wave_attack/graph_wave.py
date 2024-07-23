import matplotlib.pyplot as plt
import numpy as np
import sys
import mplcursors
import pickle
from math import sqrt

config_count = int(sys.argv[2])
N_count = int(sys.argv[3])

# first list is wave length, second is max disturbance in wave, thrid is max disturbance of all
configList = [[[], None] for _ in range(config_count)]

with open(sys.argv[1]) as f:
    for config in range(config_count):
        for n in range(N_count):
            line = f.readline()
            count, _ = line.split(" ")
            configList[config][0].append(int(count))
        line = f.readline()
        count, x = line.split(" ")
        configList[config][1] = (int(x), int(count))

fig, ax = plt.subplots()
x = np.arange(1, N_count + 1, 1, dtype=int)
ax.set_yticks(np.arange(0, 100, step=1))
ax.set_xticks(np.arange(x[0], x[-1] + 2, step=100))
ax.grid(axis="y")
xticks = ax.get_xticks()
yticks = ax.get_yticks()



for i in range(config_count):
    plt.plot(x, configList[i][0])

fig.set_size_inches(10, 6)

plt.legend([f"PRAC-{2 ** i} MAX=(Wave_Len: {configList[i][1][0]}, Disturbance: {configList[i][1][1]})" for i in range(config_count)], loc='lower right')
plt.xlabel('Wave Length', fontsize=16)
plt.ylabel('Max Disturbance', fontsize=16)
plt.title('Maximum Disturbance for Wave Attack Patterns\nBlast Radius = 2, N_BO=1', fontsize=20)
# pickle.dump(fig, open('Wave_Graph.pickle', 'wb'))
plt.show()