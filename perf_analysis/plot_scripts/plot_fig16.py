import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import warnings

methods_interested = ["QPRAC", "QPRAC+Proactive", "QPRAC+Proactive-EA", "QPRAC-Ideal"]  # Further remove PQ-NoOp if unnecessary
# Read the CSV file
csv_path = '../results/csvs/QPRAC_PRAC_Level_Results.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"The file {csv_path} does not exist.")
df = pd.read_csv(csv_path)

df_target = df[df['workload'] == 'All (57)']
# Transform the DataFrame for plotting
df_melted = pd.melt(df_target, id_vars=['workload', 'PRAC_level'], value_vars=methods_interested, var_name='PRAC_Implementation', value_name='WS')

rename_mapping = {
    'QPRAC+Proactive': 'QPRAC+Proactive',
    'QPRAC+Proactive-EA': 'QPRAC+Proactive-EA (default)',
}
df_melted['PRAC_Implementation'] = df_melted['PRAC_Implementation'].replace(rename_mapping)
# Calculate performance overhead
df_melted['Performance_Overhead'] = (1 - df_melted['WS'])*100

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

methods_interested = ["QPRAC", "QPRAC+Proactive", 'QPRAC+Proactive-EA (default)', "QPRAC-Ideal"]
df_filtered = df_high_mpki[df_high_mpki['PRAC_Implementation'].isin(methods_interested)]
df_filtered['PRAC_Implementation'] = pd.Categorical(df_filtered['PRAC_Implementation'], categories=methods_interested, ordered=True)

# Set up the plotting environment
sns.set_palette('tab10')
sns.set_style("whitegrid")

# Use TrueType fonts for PDF and PS outputs
plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts for PDFs
plt.rcParams['ps.fonttype'] = 42  # TrueType fonts for PS files

# Create the plot
fig, ax = plt.subplots(figsize=(10, 4))
plt.rc('font', size=10)
# Use Seaborn's 'tab10' color palette
palette = sns.color_palette("tab10")
colors = {impl: palette[i % len(palette)] for i, impl in enumerate(df_filtered['PRAC_Implementation'].unique())}

# Define bar width and x-tick positions
bar_width = 0.1  # Desired smaller bar width
x_ticks = [1, 2, 4]
num_bars = len(df_filtered['PRAC_Implementation'].unique())

# Create a mapping for x-tick labels
x_tick_labels = {1: 'PRAC-1', 2: 'PRAC-2', 4: 'PRAC-4'}

# Calculate positions for bars
x_tick_positions = np.linspace(0, len(x_ticks) - 1, len(x_ticks))  # Adjust spacing here
bar_positions = {}

# Calculate bar positions
for idx, tick in enumerate(x_ticks):
    base_x = x_tick_positions[idx]
    bar_positions[tick] = [base_x - (bar_width * num_bars) / 2 + j * bar_width for j in range(num_bars)]

# Add text on bars where the value is 0
for tick in x_ticks:
    subset = df_filtered[df_filtered['PRAC_level'] == tick]
    for i, prac_impl in enumerate(df_filtered['PRAC_Implementation'].unique()):
        value = subset[subset['PRAC_Implementation'] == prac_impl]['Performance_Overhead'].values[0]
        x_position = bar_positions[tick][i] + bar_width / 2  # Adjust position for centering
        color = colors[prac_impl]
        # Plot the bar
        bar = ax.bar(x_position, value, width=bar_width, color=color, edgecolor='black', label=prac_impl if tick == x_ticks[0] else "")
        # Add text if the value is 0
        if value == 0:
            ax.text(x_position, 0, '0', ha='center', va='bottom', fontsize=16, color='red')



# ax.legend(by_label.values(), by_label.keys(), loc='best', ncol=1, fancybox=True, shadow=False, fontsize=15)
ax.legend(loc='best', ncol=2, fancybox=True, shadow=False, fontsize=15)

# Set xticks to specific num_RFM values and ensure correct spacing
ax.set_xticks(x_tick_positions)
ax.set_xticklabels([x_tick_labels[tick] for tick in x_ticks])  # Use mapped labels
ax.axvline(x=0.5, color='grey', linestyle='-', alpha=0.5)
ax.axvline(x=1.5, color='grey', linestyle='-', alpha=0.5)
ax.set_xlabel('Number of RFMs per Alert Back-Off', fontsize=22)
ax.set_ylabel('Performance \nOverhead (%)', fontsize=22)
ax.tick_params(axis='both', which='major', labelsize=20)
ax.set_ylim(0, 1.16)
ax.set_xlim(-0.5, 2.5)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

plt.tight_layout()

# Ensure the results/csvs directory exists
plots_dir = '../results/plots'
os.makedirs(plots_dir, exist_ok=True)

fig.savefig(os.path.join(plots_dir, 'Figure_16.pdf'), dpi=600, bbox_inches='tight')
print(f"Figure 16 Generated")