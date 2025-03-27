import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import warnings

methods_interested = ['Cached_R', 'Cached_W', 'Cached_RW']  # Further remove PQ-NoOp if unnecessary
# Read the CSV file
csv_path = '../results/csvs/QPRAC_32_and_1024_RW_1K.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"The file {csv_path} does not exist.")
df = pd.read_csv(csv_path)

# Transform the DataFrame for plotting
df_melted = pd.melt(df, id_vars=['workload'], value_vars=methods_interested, var_name='RWs', value_name='vals')
rename_mapping = {
    'Cached_R': 'R',
    'Cached_W': 'W',
    'Cached_RW': 'RW',
}
df_melted['RWs'] = df_melted['RWs'].replace(rename_mapping)

# Filter the data for high MPKI workloads
workloads_high_mpki = [
    'ycsb_cserver', '510.parest', 'ycsb_bserver', 'ycsb_eserver', 'tpcc64', 'ycsb_aserver',
    '557.xz', '482.sphinx3', 'jp2_decode', '505.mcf', 'wc_8443', 'wc_map0', '436.cactusADM',
    '471.omnetpp', '473.astar', 'jp2_encode', 'tpch17', '483.xalancbmk', '462.libquantum',
    'tpch2', '433.milc', '520.omnetpp', '437.leslie3d', '450.soplex', '459.GemsFDTD',
    '549.fotonik3d', '434.zeusmp', '519.lbm', '470.lbm', '429.mcf', '',
    'SPEC2K6 (23)', 'SPEC2K17 (18)', 'TPC (4)', 'Hadoop (3)', 'MediaBench (3)', 
    'YCSB (6)', 'All (57)'
]
df_high_mpki = df_melted[df_melted['workload'].isin(workloads_high_mpki)]

methods_interested = ['R', 'W', 'RW']
df_filtered = df_high_mpki[df_high_mpki['RWs'].isin(methods_interested)]
df_filtered['RWs'] = pd.Categorical(df_filtered['RWs'], categories=methods_interested, ordered=True)
print(df_filtered)

# Set up the plotting environment
sns.set_palette('tab10')
sns.set_style("whitegrid")

# Use TrueType fonts for PDF and PS outputs
plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts for PDFs
plt.rcParams['ps.fonttype'] = 42  # TrueType fonts for PS files

# Create the plot
fig, ax = plt.subplots(figsize=(12, 3.7))
plt.rc('font', size=10)
xtick_order = workloads_high_mpki

ax = sns.barplot(x='workload', y='vals', hue='RWs', data=df_filtered, order=xtick_order, edgecolor='black')
ax.set_xticks(np.arange(len(xtick_order)))
ax.set_xticklabels(xtick_order, ha='right', rotation=45, fontsize=11)

# Highlight geomean labels in bold
geomean_labels = ['SPEC2K6 (23)', 'SPEC2K17 (18)', 'TPC (4)', 'Hadoop (3)', 'MediaBench (3)', 'YCSB (6)', 'All (57)']
tick_labels = ax.get_xticklabels()
for tick_label in tick_labels:
    if tick_label.get_text() in geomean_labels:
        tick_label.set_fontweight('bold')

# Add reference lines and labels
ax.axhline(y=1.0, color='r', linestyle='-', linewidth=2)
ax.axvline(30, 0, 1, color='red', linestyle='--', linewidth=2)
ax.text(33.5, 1.1, 'GMEAN', fontweight='bold')
ax.set_yticks([x / 100 for x in range(0, 101, 20)], [str(x) + "%" for x in range(0, 101, 20)])

ax.set_xlabel('')
ax.set_ylabel('Normalized Reduction', fontsize=12)
ax.legend(loc='upper right', bbox_to_anchor=(0.85, 1.27), ncol=5, fancybox=True, shadow=False, fontsize=12)
ax.set_ylim(0, 1.08)

# Final touches and save the plot
plt.grid(True, linestyle=':')
plt.title("Reduction of Read & Writes to Counter Subarray in Presence of Cache\nConfig: QPRAC+Proactive-EA, |PSQ|=32, |$|=256x4", loc='left')
plt.tight_layout()
plt.show()

# Ensure the results/csvs directory exists
plots_dir = '../results/plots'
os.makedirs(plots_dir, exist_ok=True)

fig.savefig(os.path.join(plots_dir, 'Figure_RW_1K.pdf'), dpi=600, bbox_inches='tight')
print(f"Figure Cache Hit Rate Generated")
