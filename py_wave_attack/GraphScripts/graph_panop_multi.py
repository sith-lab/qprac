import matplotlib.pyplot as plt
import numpy as np
import sys
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
panop_result1 = sys.argv[2]
panop_result2 = sys.argv[3]
panop_list = get_panop_res_list(panop_result)
panop_list1 = get_panop_res_list(panop_result1)
panop_list2 = get_panop_res_list(panop_result2)

# Sample data
categories = [i for i in range(4, 17)]

# Setting the positions and width for the bars
bar_width = 0.13
r1 = np.arange(len(categories))
r1 = [x - 0.13 for x in r1]
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

fig,ax = plt.subplots()
fig.set_size_inches(10, 3)
for x in ax.spines.values():
    x.set_alpha(0.5)
    x.set_edgecolor('grey') 
ax.tick_params(axis='both', which='major', labelsize=16, left=False)
ax.tick_params(axis='both', which='minor', labelsize=16, left=False)
# Creating the bar plot
plt.bar(r1, panop_list, width=bar_width, label='t bit = 6', edgecolor = "black",linewidth=1,zorder=3)
plt.bar(r2, panop_list1, width=bar_width, label='t bit = 8', edgecolor = "black",linewidth=1,zorder=3)
plt.bar(r3, panop_list2, width=bar_width, label='t bit = 10', edgecolor = "black",linewidth=1,zorder=3)

# # Adding labels
# plt.xlabel('Back-Off Threshold, $N_{BO}$', fontsize=22)
plt.xlabel('Service Queue Size', fontsize=22)
plt.ylabel('Maximum Unmitigated\nActivations to a Row', fontsize=20)
plt.xticks([r for r in range(len(categories))], categories)
plt.yticks([20*1024, 40*1024, 60*1024, 80*1024, 100*1024, 120*1024], [f"{i}K" for i in [20, 40, 60, 80, 100, 120]])
plt.grid(axis='y', color='grey', linestyle='-', alpha=0.5, zorder=0)

# Adding legend
handles, labels = ax.get_legend_handles_labels()
plt.legend(
    loc="upper center",
    fontsize=16,
    ncols=5,
    bbox_to_anchor=(0.5, 1.24))

plt.show()

fig.savefig("../Graphs/Panop.pdf", transparent=True, format="pdf", bbox_inches="tight")
