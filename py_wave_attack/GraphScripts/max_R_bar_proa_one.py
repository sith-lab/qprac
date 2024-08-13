import matplotlib.pyplot as plt
import numpy as np
import sys
import math
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

fig, ax = plt.subplots(1, 3)
fig.set_size_inches(15, 5)
cmap = plt.get_cmap("tab10")
for a in ax:
    a.tick_params(axis='both', which='major', labelsize=20, left=False)
    a.tick_params(axis='both', which='minor', labelsize=20, left=False)
# Creating the bar plot
# plt.bar(r1, values1, width=bar_width, color='grey', label=f'QPRAC-{PRAC_N}', edgecolor = "black",zorder=3)
# plt.bar(r2, values2, width=bar_width, color=cmap(0), label=f'QPRAC-{PRAC_N}+Proactive', edgecolor = "black",zorder=3)
markerSize = 10
ax[0].plot(np.arange(9), values1, lw=2, color='grey', label=f'QPRAC-1',marker='o', markersize=markerSize)
ax[0].plot(np.arange(9), values4, lw=2, color=cmap(0), label=f'QPRAC-1+Proactive',marker='s', markersize=markerSize)
ax[1].plot(np.arange(9), values2, lw=2, color='grey', label=f'QPRAC-2',marker='o', markersize=markerSize)
ax[1].plot(np.arange(9), values5, lw=2, color=cmap(1), label=f'QPRAC-2+Proactive',marker='s', markersize=markerSize)
ax[2].plot(np.arange(9), values3, lw=2, color='grey', label=f'QPRAC-4',marker='o', markersize=markerSize)
ax[2].plot(np.arange(9), values6, lw=2, color=cmap(2), label=f'QPRAC-4+Proactive',marker='s', markersize=markerSize)
# # Adding labels
# plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
ax[0].set_ylabel('Maximum R$_1$', fontsize=26, labelpad=10)
ax[1].set_xlabel('Back-Off Threshold, N$_{BO}$', fontsize=26, labelpad=10)
for a in ax:
    a.set_xticks(np.arange(9), categories, rotation=45)
    a.set_yticks([0] + [1024 * i for i in range(10, 71, 10)], [0] + [f"{i}K" for i in range(10, 71, 10)])


# rects = ax.patches
# which=[43, 44]
# for index, rect in enumerate(rects):
#     if index in which:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width() / 2, height + 5, height,
#                 ha='center', va='bottom', fontsize=16, c='r')

# Adding legend
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
# handles, labels = ax.get_legend_handles_labels()
# plt.legend(flip(handles, 3), flip(labels, 3), loc="upper center",
#     fontsize=16,
#     ncols=2,
#     bbox_to_anchor=(0.5, 1.39))
# Showing the plot
plt.show()

fig.savefig(f"Graphs/R1_single.pdf", transparent=True, format="pdf", bbox_inches="tight")
