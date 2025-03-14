import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import warnings

methods_interested = ["RFMsb-1", "RFMsb-2", "RFMsb-5", "RFMsb-10", 'RFMsb-17', 'RFMsb-22',
                      'RFMsb-43', 'RFMsb-45', "QPRAC-64", "QPRAC-128", "QPRAC-256", 'QPRAC-512', 'QPRAC-1024']
# Read the CSV file
csv_path = '../results/csvs/QPRAC_In_DRAM_Mitigation_Comparison.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"The file {csv_path} does not exist.")
df = pd.read_csv(csv_path)

df_target = df[df['workload'] == 'All (57)']

# Extract values from df_target
row = df_target.iloc[0]  # Extract the first row as a Series

# Create the new dataframe
new_data = {
    'TRH': [64, 128, 256, 512, 1024],
    'Mithril': [row['RFMsb-1'], row['RFMsb-2'], row['RFMsb-5'], row['RFMsb-17'], row['RFMsb-43']],
    'PrIDE': [row['RFMsb-2'], row['RFMsb-5'], row['RFMsb-10'], row['RFMsb-22'], row['RFMsb-45']],
    'QPRAC+Proactive': [row['QPRAC-64'], row['QPRAC-128'], row['QPRAC-256'], row['QPRAC-512'], row['QPRAC-1024']],
}
new_df = pd.DataFrame(new_data)


methods_interested = ["Mithril", 'PrIDE', 'QPRAC+Proactive']

# Transform the DataFrame for plotting
df_melted = pd.melt(new_df, id_vars=['TRH'], value_vars=methods_interested, var_name='Mitigations', value_name='WS')

rename_mapping = {
    'QPRAC+Proactive': 'QPRAC+Proactive-EA',
}
df_melted['Mitigations'] = df_melted['Mitigations'].replace(rename_mapping)

methods_interested = ["Mithril", 'PrIDE', 'QPRAC+Proactive-EA']

df_melted['Mitigations'] = pd.Categorical(df_melted['Mitigations'], categories=methods_interested, ordered=True)

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
colors = {impl: palette[i % len(palette)] for i, impl in enumerate(df_melted['Mitigations'].unique())}

# Define bar width and x-tick positions
bar_width = 0.1  # Desired smaller bar width
x_ticks = [64 ,128, 256, 512, 1024]
num_bars = len(df_melted['Mitigations'].unique())

# Calculate positions for bars
x_tick_positions = np.linspace(0, len(x_ticks) - 1, len(x_ticks))  # Adjust spacing here
bar_positions = {}

# Calculate bar positions
for idx, tick in enumerate(x_ticks):
    base_x = x_tick_positions[idx]
    bar_positions[tick] = [base_x - (bar_width * num_bars) / 2 + j * bar_width for j in range(num_bars)]

# Plot bars
for tick in x_ticks:
    subset = df_melted[df_melted['TRH'] == tick]
    for i, prac_impl in enumerate(df_melted['Mitigations'].unique()):
        value = subset[subset['Mitigations'] == prac_impl]['WS'].values[0]
        x_position = bar_positions[tick][i] + bar_width / 2  # Adjust position for centering
        color = colors[prac_impl]
        ax.bar(x_position, value, width=bar_width, color=color, edgecolor='black', label=prac_impl if tick == x_ticks[0] else "")

# Add a horizontal line at y=1.0
ax.axhline(y=1.0, color='r', linestyle='-', linewidth=2)
# Customize legend, labels, and ticks
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # Remove duplicate labels from the legend
ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, 1.26), ncol=3, fancybox=True, shadow=False, fontsize=17)

# Set xticks to specific num_RFM values and ensure correct spacing
ax.set_xticks(x_tick_positions)
ax.set_xticklabels(x_ticks)
ax.axvline(x=0.5, color='grey', linestyle='-', alpha=0.5)
ax.axvline(x=1.5, color='grey', linestyle='-', alpha=0.5)
ax.axvline(x=2.5, color='grey', linestyle='-', alpha=0.5)
ax.axvline(x=3.5, color='grey', linestyle='-', alpha=0.5)
ax.set_xlabel('Supported RowHammer Threshold (T$_{RH}$)', fontsize=22)
ax.set_ylabel('Normalized \nPerformance', fontsize=22)
ax.tick_params(axis='both', which='major', labelsize=20)
ax.set_ylim(0, 1.02)
ax.set_xlim(-0.5, 4.5)

ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
plt.tight_layout()

# Ensure the results/csvs directory exists
plots_dir = '../results/plots'
os.makedirs(plots_dir, exist_ok=True)

fig.savefig(os.path.join(plots_dir, 'Figure_20.pdf'), dpi=600, bbox_inches='tight')
print(f"Updated Figure 20 Generated")
