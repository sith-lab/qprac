import matplotlib.pyplot as plt
import numpy as np
import sys

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
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
# Creating the bar plot
for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey') 
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5,zorder=0)
plt.bar(r1, values1, width=bar_width, label='PRAC-1', edgecolor = "black", linewidth=1,zorder=3)
plt.bar(r2, values2, width=bar_width, label='PRAC-2', edgecolor = "black", linewidth=1,zorder=3)
plt.bar(r3, values3, width=bar_width, label='PRAC-4', edgecolor = "black", linewidth=1,zorder=3)

# # Adding labels
# plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
plt.ylabel('Maximum R$_1$', fontsize=22)
plt.xlabel('Back-Off Threshold, N$_{BO}$', fontsize=22)
plt.xticks([r + bar_width for r in range(len(categories))], categories)
plt.yticks([10*1024,20*1024, 30*1024, 40*1024, 50*1024, 60*1024], [f"{i}K" for i in [10, 20, 30, 40, 50, 60]])

# Adding legend
plt.legend(fontsize=16,
    ncols=3)

fig.savefig("figure7.pdf", transparent=True, format="pdf", bbox_inches="tight")
