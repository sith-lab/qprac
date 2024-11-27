import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import itertools

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])
def get_panop_res_list(filename):
    panop_lists = []
    with open(filename) as f:
        for line in f:
            act = int(line.strip())
            panop_lists.append(act)
    return panop_lists

panop_result = sys.argv[1]
panop_list = get_panop_res_list(panop_result)

# Sample data
categories = [i for i in range(4, 17)]

# Setting the positions and width for the bars
bar_width = 0.3
r1 = np.arange(len(categories))
print(panop_list)
print(categories)
print(r1)

fig,ax = plt.subplots()
fig.set_size_inches(10, 4)
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey') 
# Creating the bar plot
plt.bar(r1, panop_list, width=bar_width, edgecolor = "black", linewidth=1, zorder=3)

# # Adding labels
plt.xlabel('FIFO-based Service Queue Size', fontsize=22)
plt.ylabel('Maximum Unmitigated\nActivations to a Row', fontsize=22)
plt.xticks([r for r in range(len(categories))], categories)
plt.yticks([20*1024, 40*1024, 60*1024, 80*1024, 100*1024, 120*1024], [f"{i}K" for i in [20, 40, 60, 80, 100, 120]])
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5, zorder=0)
# Adding legend
# handles, labels = ax.get_legend_handles_labels()
# plt.legend(loc="upper center",
#     fontsize=16,
#     ncols=5,
#     bbox_to_anchor=(0.5, 1.24))
# Showing the plot

plt.show()

fig.savefig("Graphs/Panop.pdf", transparent=True, format="pdf", bbox_inches="tight")
