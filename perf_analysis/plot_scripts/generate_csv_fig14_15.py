import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

multi_cores_out_path = '../results'

df = pd.DataFrame(columns=["workload"])
mitigation_list = ["Baseline", "QPRAC-NoOp","QPRAC", "QPRAC+Proactive", "QPRAC-Ideal"]
for mitigation in mitigation_list:
    result_path = multi_cores_out_path + "/" + mitigation +"/stats/"
    result_list = [x[:-4] for x in os.listdir(result_path) if x.endswith(".txt")]
    for result_filename in result_list:
        # Process only files starting with '32_'
        if mitigation == "Baseline" and not result_filename.startswith("32_"):
            continue
        result_file = open(result_path + result_filename + ".txt", "r")
        NBO = int(result_filename.split("_")[0])
        if NBO != 32:
            continue
        prac_level = int(result_filename.split("_")[1])
        if prac_level != 1:
            continue
        psq_size = int(result_filename.split("_")[2])
        if psq_size != 5:
            continue
        targeted_ref_ratio = int(result_filename.split("_")[3])
        if mitigation == "QPRAC+Proactive" and not targeted_ref_ratio == 1:
            continue
        workload = "_".join(result_filename.split("_")[4:])

        w0=''
        w1=''
        w2=''
        w3=''
        ipc_0 = 0
        ipc_1 = 0
        ipc_2 = 0
        ipc_3 = 0
        cycle_0 = 0
        cycle_1 = 0
        cycle_2 = 0
        cycle_3 = 0
        num_inst_0=0
        num_inst_1=0
        num_inst_2=0
        num_inst_3=0
        num_rd_reqs=0
        num_wr_reqs=0
        wr_reqs_ratio = 0.0
        num_abo = 0
        num_tREFI_period=0
        # num_tREFW_period=0
        for line in result_file.readlines():
            if ("name_trace_0:" in line):
                w0 = str(line.split("/")[-1]).strip()
            if ("name_trace_1:" in line):
                w1 = str(line.split("/")[-1]).strip()
            if ("name_trace_2:" in line):
                w2 = str(line.split("/")[-1]).strip()
            if ("name_trace_3:" in line):
                w3 = str(line.split("/")[-1]).strip()
            if (" cycles_recorded_core_0:" in line):
                cycle_0 = int(line.split(" ")[-1])
            if (" cycles_recorded_core_1:" in line):
                cycle_1 = int(line.split(" ")[-1])
            if (" cycles_recorded_core_2:" in line):
                cycle_2 = int(line.split(" ")[-1])
            if (" cycles_recorded_core_3:" in line):
                cycle_3 = int(line.split(" ")[-1])
            if (" insts_recorded_core_0" in line):
                num_inst_0 = int(line.split(" ")[-1])
            if (" insts_recorded_core_1" in line):
                num_inst_1 = int(line.split(" ")[-1])
            if (" insts_recorded_core_2" in line):
                num_inst_2 = int(line.split(" ")[-1])
            if (" insts_recorded_core_3" in line):
                num_inst_3 = int(line.split(" ")[-1])
            if (" prac_num_recovery" in line):
                num_abo = int(line.split(" ")[-1])
            if (" controller0_num_refresh_reqs" in line):
                num_tREFI_period = int(line.split(" ")[-1])           
                
        if (cycle_0 == 0 and cycle_1 == 0 and cycle_2 == 0 and cycle_3 == 0):
            continue
        if (cycle_0 == 0 or cycle_1 == 0 or cycle_2 == 0 or cycle_3 == 0):
            print("Error: " + result_filename)
        ipc_0 = int(num_inst_0) / cycle_0
        ipc_1 = int(num_inst_1) / cycle_1
        ipc_2 = int(num_inst_2) / cycle_2
        ipc_3 = int(num_inst_3) / cycle_3
        
        WS = ipc_0 + ipc_1 + ipc_2 + ipc_3
        ABO_per_tREFI = float(num_abo)/float(num_tREFI_period/2)

        result_file.close()
        # Create a new DataFrame for the new row
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'WS': [WS],
            'ABO_per_tREFI': [ABO_per_tREFI],
        })
        df = pd.concat([df, new_row], ignore_index=True)

df_ws = df.pivot(index=['workload', 'NBO'], columns=['mitigation'], values='WS').reset_index()
df_abo = df.pivot(index=['workload', 'NBO'], columns=['mitigation'], values='ABO_per_tREFI').reset_index()
df_abo.drop(columns=['Baseline'], inplace=True)

for mitigation in set(mitigation_list) - set(['Baseline']):
    df_ws[mitigation] = df_ws[mitigation] / df_ws['Baseline']
df_ws.drop(columns=['Baseline'], inplace=True)

# print(df_ws)

benchmark_suites = {
    'SPEC2K6 (23)': ['401.bzip2', '403.gcc', '429.mcf', '433.milc', '434.zeusmp', '435.gromacs', '436.cactusADM', '437.leslie3d', '444.namd', '445.gobmk', '447.dealII', '450.soplex', '456.hmmer', '458.sjeng', '459.GemsFDTD', '462.libquantum', '464.h264ref', '470.lbm', '471.omnetpp', '473.astar', '481.wrf', '482.sphinx3', '483.xalancbmk'], # SPEC2K6: 23
    'SPEC2K17 (18)': ['500.perlbench', '502.gcc', '505.mcf', '507.cactuBSSN', '508.namd', '510.parest', '511.povray', '519.lbm', '520.omnetpp', '523.xalancbmk', '525.x264', '526.blender', '531.deepsjeng', '538.imagick', '541.leela', '544.nab', '549.fotonik3d', '557.xz'], # SPEC2K17: 18
    'TPC (4)': ['tpcc64', 'tpch17', 'tpch2', 'tpch6'], #tpc: 4
    # TODO: Enable Hadoop and LonestartGPU after fixing the performance shooting problem + h264_decode
    'Hadoop (3)': ['grep_map0', 'wc_8443', 'wc_map0'], #Hadoop: 3
    'MediaBench (3)': ['h264_encode', 'jp2_decode', 'jp2_encode'], #mediabench: 3
    'YCSB (6)': ['ycsb_abgsave', 'ycsb_aserver', 'ycsb_bserver', 'ycsb_cserver', 'ycsb_dserver', 'ycsb_eserver'] #ycsb:6
}

# Function to calculate geometric mean
def calculate_geometric_mean(series):
    return np.prod(series) ** (1 / len(series))

# Function to calculate and add geometric means as new rows
def add_geomean_rows(df):
    geomean_rows = []  # List to collect new rows

    for NBO in df['NBO'].unique():
        for suite_name, workloads in benchmark_suites.items():
            suite_df = df[(df['workload'].isin(workloads)) & (df['NBO'] == NBO)]
            if not suite_df.empty:
                geomeans = {}
                
                # Dynamically calculate geometric means for each mitigation
                for mitigation in mitigation_list:
                    if mitigation in suite_df.columns:  # Ensure the column exists
                        geomeans[mitigation] = calculate_geometric_mean(suite_df[mitigation])
                
                # Create a new row
                geomean_row = {'NBO': NBO, 'workload': suite_name, **geomeans}
                geomean_rows.append(geomean_row)  # Append to the list

    # Convert list of rows to DataFrame
    geomean_df = pd.DataFrame(geomean_rows)
    
    return pd.concat([df, geomean_df], ignore_index=True)

# Function to add combined geometric means for all workloads in each channel and interface
def add_all_workloads_geomean_rows(df):
    geomean_rows = []  # List to collect new rows
    
    for NBO in df['NBO'].unique():
            Channel_interface_df = df[(df['NBO'] == NBO)]
            geomean_values = {}

            # Calculate geometric means for each mitigation in the list
            for mitigation in mitigation_list:
                if mitigation in Channel_interface_df.columns:  # Ensure the column exists
                    geomean_values[mitigation] = calculate_geometric_mean(Channel_interface_df[mitigation])

            # Create a new row for the combined results
            geomean_row = {'NBO': NBO, 'workload': 'All (57)', **geomean_values}
            geomean_rows.append(geomean_row)  # Append to the list
    
    # Convert list of rows to DataFrame
    geomean_df = pd.DataFrame(geomean_rows)
    
    return pd.concat([df, geomean_df], ignore_index=True)

# Function to calculate geometric mean
def calculate_arithmetic_mean(series):
    return series.mean()

# Function to calculate and add geometric means as new rows
def add_arithmetic_mean_rows(df):
    amean_rows = []  # List to collect new rows

    for NBO in df['NBO'].unique():
        for suite_name, workloads in benchmark_suites.items():
            suite_df = df[(df['workload'].isin(workloads)) & (df['NBO'] == NBO)]
            if not suite_df.empty:
                ameans = {}
                
                # Dynamically calculate geometric means for each mitigation
                for mitigation in mitigation_list:
                    if mitigation in suite_df.columns:  # Ensure the column exists
                        ameans[mitigation] = calculate_arithmetic_mean(suite_df[mitigation])
                
                # Create a new row
                amean_row = {'NBO': NBO, 'workload': suite_name, **ameans}
                amean_rows.append(amean_row)  # Append to the list

    # Convert list of rows to DataFrame
    amean_df = pd.DataFrame(amean_rows)
    
    return pd.concat([df, amean_df], ignore_index=True)

# Function to add combined geometric means for all workloads in each channel and interface
def add_all_workloads_amean_rows(df):
    amean_rows = []  # List to collect new rows
    
    for NBO in df['NBO'].unique():
            Channel_interface_df = df[(df['NBO'] == NBO)]
            amean_values = {}

            # Calculate geometric means for each mitigation in the list
            for mitigation in mitigation_list:
                if mitigation in Channel_interface_df.columns:  # Ensure the column exists
                    amean_values[mitigation] = calculate_arithmetic_mean(Channel_interface_df[mitigation])

            # Create a new row for the combined results
            amean_row = {'NBO': NBO, 'workload': 'All (57)', **amean_values}
            amean_rows.append(amean_row)  # Append to the list
    
    # Convert list of rows to DataFrame
    amean_df = pd.DataFrame(amean_rows)
    
    return pd.concat([df, amean_df], ignore_index=True)

mitigation_list = ["QPRAC-NoOp","QPRAC", "QPRAC+Proactive", "QPRAC-Ideal"]
new_column_order = ['workload', 'NBO'] + mitigation_list

geomean_df = add_geomean_rows(df_ws)
geomean_df = add_all_workloads_geomean_rows(geomean_df)
geomean_df = geomean_df[new_column_order]

amean_df = add_arithmetic_mean_rows(df_abo)
amean_df = add_all_workloads_amean_rows(amean_df)
amean_df = amean_df[new_column_order]
# Ensure the results/csvs directory exists
csv_dir = '../results/csvs'
os.makedirs(csv_dir, exist_ok=True)

# Save the CSV file
geomean_df.to_csv(os.path.join(csv_dir, 'QPRAC_32NBO_5PSQ_results.csv'), index=False)
amean_df.to_csv(os.path.join(csv_dir, 'QPRAC_ABO_results.csv'), index=False)