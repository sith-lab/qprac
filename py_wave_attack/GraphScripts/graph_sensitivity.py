import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import matplotlib.ticker as mtick
import itertools

def load_sense_NBO(filename):
    len_list = [[], [], [], []]
    with open(filename) as f:
        for i in range(0, 4):
            for _ in range(0, 4):
                line = f.readline().strip()
                perc = line
                len_list[i].append(float(perc))
    return len_list

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

len_file = sys.argv[1]
len_list = load_sense_NBO(len_file)

# Sample data
categories = [2 ** size for size in range(4, 8)]
values1 = len_list[0]
values2 = len_list[1]
values3 = len_list[2]
values4 = len_list[3]

# Setting the positions and width for the bars
bar_width = 0.1
r1 = np.arange(len(categories))
r1 = [x - 0.05 for x in r1]
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

fig,ax = plt.subplots()
fig.set_size_inches(10, 3)
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey') 
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5,zorder=0)
# Creating the bar plot
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.bar(r1, values1, width=bar_width, label='QPRAC-RFM$_{ab}$', edgecolor = "black",zorder=3)
plt.bar(r2, values2, width=bar_width, label='QPRAC-RFM$_{ab}$+Proactive (default)', edgecolor = "black",zorder=3)
plt.bar(r3, values3, width=bar_width, label='QPRAC-RFM$_{sb}$+Proactive', edgecolor = "black",zorder=3)
plt.bar(r4, values4, width=bar_width, label='QPRAC-RFM$_{pb}$+Proactive', edgecolor = "black",zorder=3)
# # Adding labels
# plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
plt.ylabel('Bandwidth Reduction', fontsize=22)
plt.xlabel('Back-Off Threshold (N$_{BO})$', fontsize=22)
plt.yticks([0, 20, 40, 60, 80, 100])
plt.xticks([r + bar_width for r in range(len(categories))], categories)
# plt.yticks([10*1024,20*1024, 30*1024, 40*1024, 50*1024, 60*1024], [f"{i}K" for i in [10, 20, 30, 40, 50, 60]])

rects = ax.patches
NA=[]
ZERO=[7,11,15]
for index, rect in enumerate(rects):
    if index in NA or index in ZERO:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, 0 if index in ZERO else "N/A",
                ha='center', va='bottom', fontsize=14, c='r')        
# Adding legend
handles, labels = ax.get_legend_handles_labels()
plt.legend(flip(handles, 2), flip(labels, 2),fontsize=16,
    ncols=2
    ,loc="upper center",
    bbox_to_anchor=(0.5, 1.43)
    )

# Showing the plot
plt.show()

fig.savefig("Graphs/Sensitivity.pdf", transparent=True, format="pdf", bbox_inches="tight")
