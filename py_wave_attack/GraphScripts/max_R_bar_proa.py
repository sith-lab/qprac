import matplotlib.pyplot as plt
import numpy as np
import sys
import itertools

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

def load_len_NBO_reac(filename):
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

len_file = sys.argv[1]
len_file_proa = sys.argv[2]
len_N1, len_N2, len_N4 = load_len_NBO_reac(len_file)
len_N1_pro, len_N2_pro, len_N4_pro = load_len_NBO_proa(len_file_proa)
# Sample data
categories = [2 ** size for size in range(0, 9)]
values1 = [len for _, len in len_N1]
values2 = [len for _, len in len_N2]
values3 = [len for _, len in len_N4]
values4 = [len for _, len in len_N1_pro]
values5 = [len for _, len in len_N2_pro]
values6 = [len for _, len in len_N4_pro]

# Setting the positions and width for the bars
bar_width = 0.13
r1 = np.arange(len(categories))
r1 = [x - 0.195 for x in r1]
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3] 
r5 = [x + bar_width for x in r4]
r6 = [x + bar_width for x in r5]

fig,ax = plt.subplots()
fig.set_size_inches(10, 3)
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
# Creating the bar plot
plt.bar(r1, values1, width=bar_width, color='lightgrey', label='QPRAC-1', edgecolor = "black",zorder=3)
plt.bar(r2, values2, width=bar_width, color='grey', label='QPRAC-2', edgecolor = "black",zorder=3)
plt.bar(r3, values3, width=bar_width, color='black', label='QPRAC-4', edgecolor = "black",zorder=3)
plt.bar(r4, values4, width=bar_width, label='QPRAC-1+Proactive', edgecolor = "black",zorder=3)
plt.bar(r5, values5, width=bar_width, label='QPRAC-2+Proactive', edgecolor = "black",zorder=3)
plt.bar(r6, values6, width=bar_width, label='QPRAC-4+Proactive', edgecolor = "black",zorder=3)

# # Adding labels
# plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
plt.ylabel('Maximum R$_1$', fontsize=22)
plt.xlabel('Back-Off Threshold, N$_{BO}$', fontsize=22)
plt.xticks([r + bar_width for r in range(len(categories))], categories)
plt.yticks([1024 * i for i in range(10, 71, 10)],  [f"{i}K" for i in range(10, 71, 10)])

for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey') 
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5,zorder=0)
rects = ax.patches
which=[43, 44]
for index, rect in enumerate(rects):
    if index in which:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 5, height,
                ha='center', va='bottom', fontsize=16, c='r')

# Adding legend
plt.legend(fontsize=15,
    ncols=1,
    bbox_to_anchor=(1.01, 1.04))
# handles, labels = ax.get_legend_handles_labels()
# plt.legend(flip(handles, 3), flip(labels, 3), loc="upper center",
#     fontsize=16,
#     ncols=2,
#     bbox_to_anchor=(0.5, 1.39))
# Showing the plot
plt.show()

fig.savefig("Graphs/R1_vs_NBO_PROA.pdf", transparent=True, format="pdf", bbox_inches="tight")
