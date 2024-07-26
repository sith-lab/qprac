import matplotlib.pyplot as plt
import numpy as np
import sys
import math

def load_len_NBO(filename):
    len_list = [[], [], []]
    with open(filename) as f:
        for rfm in range(0, 3):
            for nbo in [2 ** size for size in range(0, 9)]:
                line = f.readline().strip()
                wave_len, _ = line.split(" ")
                len_list[rfm].append((int(nbo), int(wave_len)))
    return len_list


len_file = sys.argv[1]
len_N1, len_N2, len_N4 = load_len_NBO(len_file)

# Sample data
categories = [2 ** size for size in range(0, 9)]
values1 = [len for _, len in len_N1]
values2 = [len for _, len in len_N2]
values3 = [len for _, len in len_N4]

# Setting the positions and width for the bars
bar_width = 0.2
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

fig,ax = plt.subplots()
fig.set_size_inches(10, 3)
ax.tick_params(axis='both', which='major', labelsize=16)
ax.tick_params(axis='both', which='minor', labelsize=16)
# Creating the bar plot
plt.bar(r1, values1, width=bar_width, label='PRAC-1', edgecolor = "black", linewidth=1.5)
plt.bar(r2, values2, width=bar_width, label='PRAC-2', edgecolor = "black", linewidth=1.5)
plt.bar(r3, values3, width=bar_width, label='PRAC-4', edgecolor = "black", linewidth=1.5)

# # Adding labels
# plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
plt.ylabel('Max $R_1$', fontsize=22)
plt.xticks([r + bar_width for r in range(len(categories))], categories)
plt.yticks([5000, 10000,20000,40000,60000], [f"{i}k" for i in [5, 10, 20, 40, 60]])
plt.grid(axis='y', linestyle='--', color='black', alpha=0.7)

# Adding legend
plt.legend(fontsize=16,
    ncols=3)

# Showing the plot
plt.show()

fig.savefig("R1_vs_NBO.pdf", transparent=True, format="pdf", bbox_inches="tight")