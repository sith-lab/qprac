import matplotlib.pyplot as plt
import numpy as np
import sys
import mplcursors
import pickle
from math import sqrt
import matplotlib.patheffects as pe
import itertools

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

config_count = int(sys.argv[2])
N_count = int(sys.argv[3])

# first list is wave length, second is max disturbance in wave, thrid is max disturbance of all
configList = [[[], None] for _ in range(config_count)]

with open(sys.argv[1]) as f:
    for config in range(config_count):
        for n in range(N_count):
            line = f.readline()
            count, _ = line.split(" ")
            configList[config][0].append(int(count) - 1)
        line = f.readline()
        count, x = line.split(" ")
        configList[config][1] = (int(x), int(count) - 1)

fig, ax = plt.subplots()

x = np.arange(4, N_count + 1, 1, dtype=int)
# ax.set_yticks(np.arange(0, 50, step=5))
plt.xticks([4] + [1024 * i for i in range(20, 141, 20)], [4] + [f"{i}K" for i in range(20, 141, 20)])
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5,zorder=0)
xticks = ax.get_xticks()
yticks = ax.get_yticks()


for i in range(config_count//2):
    plt.plot(x, configList[i][0][3:], lw=2, label=f"QPRAC-{2 ** i}", linestyle='dashed')
for i in range(config_count//2):
    plt.plot(x, configList[i + config_count//2][0][3:], lw=3, c=plt.get_cmap("tab10")(i), label=f"QPRAC-{2 ** i}+Proactive")
fig.set_size_inches(10, 3)
for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey')

        # f"PRAC-{2 ** i} MAX=(Wave_Len: {configList[i][1][0]}, Disturbance: {configList[i][1][1]})"
        # for i in range(config_count)

handles, labels = ax.get_legend_handles_labels()
# leg = plt.legend(
#     [
#     f"PRAC-{2 ** i}-EXACT" for i in range(config_count//2)
#     ] + [f"PRAC-{2 ** i}-EST" for i in range(config_count//2)],
#     loc="upper center",
#     fontsize=16,
#     ncols=3
#     )

leg = plt.legend(flip(handles, 3), flip(labels, 3), loc="upper center",
    fontsize=16,
    ncols=3,
    bbox_to_anchor=(0.5, 1.39))
for line in leg.get_lines():
    line.set_linewidth(4.0)
plt.xlabel('Row Pool Size, R$_1$', fontsize=22)
plt.ylabel("N$_{online}$", fontsize=22)
# plt.title('Maximum Disturbance for Wave Attack Pattern\nBlast Radius = 2, N_BO=1', fontsize=20)
plt.savefig("Graphs/N_Online_VS_PRAC_N_PROA.pdf", transparent=True, format="pdf", bbox_inches="tight")
plt.show()
