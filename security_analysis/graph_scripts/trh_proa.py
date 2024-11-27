import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import itertools

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

def load_max_dist_map(filename):
    dist_map = [{}, {}, {}, {}, {}, {}]
    with open(filename) as f:
        for rfm in range(0, 6):
            for n in range(131072):
                line = f.readline().strip()
                act, wave_len = line.split(" ")
                dist_map[rfm][(2 ** (rfm % 3), int(wave_len))] = int(act)
            f.readline()
    return dist_map

def load_len_NBO(filename):
    len_list = [[], [], []]
    with open(filename) as f:
        for rfm in range(0, 3):
            for nbo in [2 ** size for size in range(0, 9)]:
                line = f.readline().strip()
                wave_len, _ = line.split(" ")
                len_list[rfm].append((int(nbo), int(wave_len)))
    return len_list

def load_len_NBO_proa(filename):
    len_list = [[], [], []]
    with open(filename) as f:
        for rfm in range(0, 3):
            for nbo in [2 ** size for size in range(0, 9)]:
                line = f.readline().strip()
                wave_len, deduc, _, _ = line.split(" ")
                true_wave_len = int(wave_len) - int(deduc)
                if true_wave_len < 0:
                    true_wave_len = 0
                len_list[rfm].append((int(nbo), true_wave_len))
    return len_list

def get_max_dist(map, N, len):
    if ((N, len) in map):
        max = map[(N, len)]
        for i in range(0, 5):
            if len - i >= 0:
                if map[(N, len - i)] > max:
                    max = map[(N, len - i)]
        return max
    else:
        return 0
dist_map_file = sys.argv[1]
len_file = sys.argv[2]
len_file_proa = sys.argv[3]
max_dist_1, max_dist_2, max_dist_4, max_dist_1_proa, max_dist_2_proa, max_dist_4_proa = load_max_dist_map(dist_map_file)
len_N1, len_N2, len_N4 = load_len_NBO(len_file)
len_N1_proa, len_N2_proa, len_N4_proa = load_len_NBO_proa(len_file_proa)

# Sample data
categories = [2 ** size for size in range(0, 9)]
Y_categories = [2 ** size for size in range(4, 10)]
values1 = [get_max_dist(max_dist_1, 1, len) for _, len in len_N1]
values2 = [get_max_dist(max_dist_2, 2, len) for _, len in len_N2]
values3 = [get_max_dist(max_dist_4, 4, len) for _, len in len_N4]
values4 = [get_max_dist(max_dist_1_proa, 1, len) for _, len in len_N1_proa]
values5 = [get_max_dist(max_dist_2_proa, 2, len) for _, len in len_N2_proa]
values6 = [get_max_dist(max_dist_4_proa, 4, len) for _, len in len_N4_proa]
for size in range(0, 9):
    for vlist in [values1, values2, values3, values4, values5, values6]:
        vlist[size] = math.log(vlist[size] + 2 ** size, 2)

# Setting the positions and width for the bars

fig, ax = plt.subplots(1, 3)
fig.set_size_inches(15, 5)
cmap = plt.get_cmap("tab10")
for a in ax:
    a.tick_params(axis='both', which='major', labelsize=20, left=False)
    a.tick_params(axis='both', which='minor', labelsize=20, left=False)
# Creating the bar plot

markerSize = 10
ax[0].plot(np.arange(9), values1, lw=2, color='grey', label=f'QPRAC-1',marker='o', markersize=markerSize)
ax[0].plot(np.arange(9), values4, lw=2, color=cmap(0), label=f'QPRAC-1+Proactive',marker='s', markersize=markerSize)
ax[1].plot(np.arange(9), values2, lw=2, color='grey', label=f'QPRAC-2',marker='o', markersize=markerSize)
ax[1].plot(np.arange(9), values5, lw=2, color=cmap(1), label=f'QPRAC-2+Proactive',marker='s', markersize=markerSize)
ax[2].plot(np.arange(9), values3, lw=2, color='grey', label=f'QPRAC-4',marker='o', markersize=markerSize)
ax[2].plot(np.arange(9), values6, lw=2, color=cmap(2), label=f'QPRAC-4+Proactive',marker='s', markersize=markerSize)

# # Adding labels
ax[0].set_ylabel('T$_{RH}$', fontsize=26, labelpad=10)
ax[1].set_xlabel('Back-Off Threshold, N$_{BO}$', fontsize=26, labelpad=10)
for a in ax:
    a.set_xticks(np.arange(9), categories, rotation=45)
    a.set_yticks([size for size in range(4, 10)], Y_categories)

for a in ax:
    for x in a.spines.values():
        x.set_alpha(0.5)
        x.set_edgecolor('grey') 
    a.grid(axis='y', color='grey', linestyle='-', alpha=0.5,zorder=0)
    leg = a.legend(fontsize=20,
        ncols=1,
        bbox_to_anchor=(0.5, 1.36),
        loc="upper center")
    for line in leg.get_lines():
        line.set_linewidth(3.0)
plt.show()

fig.savefig("./output/graphs/TRH_single.pdf", transparent=True, format="pdf", bbox_inches="tight")
