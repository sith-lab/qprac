import matplotlib.pyplot as plt
import numpy as np
import sys

config_count = int(sys.argv[2])
N_count = int(sys.argv[3])

# first list is wave length, second is max disturbance in wave, thrid is max disturbance of all
configList = [[[], None] for _ in range(config_count)]

with open(sys.argv[1]) as f:
    for config in range(config_count):
        for n in range(N_count):
            line = f.readline()
            count, _ = line.split(" ")
            configList[config][0].append(int(count)-1)
        line = f.readline()
        count, x = line.split(" ")
        configList[config][1] = (int(x), int(count)-1)

fig, ax = plt.subplots()
fig.set_size_inches(10, 3)
x = np.arange(4, N_count + 1, 1, dtype=int)
ax.set_yticks(np.arange(0, 50, step=5))
plt.xticks([4] + [1024 * i for i in range(20, 141, 20)], [4] + [f"{i}K" for i in range(20, 141, 20)])
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5,zorder=0)
xticks = ax.get_xticks()
yticks = ax.get_yticks() 

for i in range(config_count):
    plt.plot(x, configList[i][0][3:], lw=3)
for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey')


leg = plt.legend(
    [
    f"PRAC-{2 ** i}" for i in range(config_count)
    ],
    loc="lower right",
    fontsize=16,
    ncols=3
    )
for line in leg.get_lines():
    line.set_linewidth(4.0)
plt.xlabel('Starting Row Pool, R$_1$', fontsize=22)
plt.ylabel("N$_{online}$", fontsize=22)
plt.show()
fig.savefig("./output/graphs/N_Online_VS_PRAC_N.pdf", transparent=True, format="pdf", bbox_inches="tight")

