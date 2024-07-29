import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import itertools
def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

def load_max_dist_map(filename):
    dist_map = [{},{},{}]
    with open(filename) as f:
        for rfm in range(0, 3):
            for n in range(65536):
                line = f.readline().strip()
                act, wave_len = line.split(" ")
                dist_map[rfm][(2 ** rfm, int(wave_len))] = int(act) -  1
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
dist_map_file_proa = sys.argv[3]
len_file_proa = sys.argv[4]
max_dist_1, max_dist_2, max_dist_4 = load_max_dist_map(dist_map_file)
len_N1, len_N2, len_N4 = load_len_NBO(len_file)
max_dist_1_proa, max_dist_2_proa, max_dist_4_proa = load_max_dist_map(dist_map_file_proa)
len_N1_proa, len_N2_proa, len_N4_proa = load_len_NBO_proa(len_file_proa)

# Sample data
categories = [2 ** size for size in range(0, 9)]
Y_categories = [2 ** size for size in range(0, 10)]
values1 = [get_max_dist(max_dist_1, 1, len) for _, len in len_N1]
values2 = [get_max_dist(max_dist_2, 2, len) for _, len in len_N2]
values3 = [get_max_dist(max_dist_4, 4, len) for _, len in len_N4]
values4 = [get_max_dist(max_dist_1_proa, 1, len) for _, len in len_N1_proa]
values5 = [get_max_dist(max_dist_2_proa, 2, len) for _, len in len_N2_proa]
values6 = [get_max_dist(max_dist_4_proa, 4, len) for _, len in len_N4_proa]

# Setting the positions and width for the bars
bar_width = 0.13
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]
r5 = [x + bar_width for x in r4]
r6 = [x + bar_width for x in r5]

fig,ax = plt.subplots()
fig.set_size_inches(10, 3)
ax.tick_params(axis='both', which='major', labelsize=16)
ax.tick_params(axis='both', which='minor', labelsize=16)
# Creating the bar plot
plt.bar(r1, values1, width=bar_width, color='lightgrey', label='PRAC-1 REA', edgecolor = "black", linewidth=1.5)
plt.bar(r2, values2, width=bar_width, color='grey', label='PRAC-2 REA', edgecolor = "black", linewidth=1.5)
plt.bar(r3, values3, width=bar_width, color='black', label='PRAC-4 REA', edgecolor = "black", linewidth=1.5)
plt.bar(r4, values4, width=bar_width, label='PRAC-1 REA + PRO', edgecolor = "black", linewidth=1.5)
plt.bar(r5, values5, width=bar_width, label='PRAC-2 REA + PRO', edgecolor = "black", linewidth=1.5)
plt.bar(r6, values6, width=bar_width, label='PRAC-4 REA + PRO', edgecolor = "black", linewidth=1.5)

# # Adding labels
plt.ylabel('Max $N_{online}$', fontsize=22)
plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
plt.xticks([r + bar_width for r in range(len(categories))], categories)
plt.grid(axis='y', linestyle='--', color='black', alpha=0.7)

# Adding legend
# plt.legend(loc='upper center', fontsize=16,
#     ncols=3,bbox_to_anchor=(0.5, 1.23))
# handles, labels = ax.get_legend_handles_labels()
# plt.legend(flip(handles, 3), flip(labels, 3), loc="upper center",
#     fontsize=16,
#     ncols=3,
#     bbox_to_anchor=(0.5, 1.39))
# Showing the plot
plt.show()

fig.savefig("Nonline_vs_NBO_PROA.pdf", transparent=True, format="pdf", bbox_inches="tight")
