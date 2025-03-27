import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

multi_cores_out_path = '../results'
PB = True
df = pd.DataFrame(columns=["workload"])
mitigation_list = ["QPRAC+Proactive-EA"]
for mitigation in mitigation_list:
    result_path = multi_cores_out_path + "/" + mitigation +"/stats/"
    result_list = [x[:-4] for x in os.listdir(result_path) if x.endswith(".txt")]
    for result_filename in result_list:
        # Process only files starting with '32_'
        if not result_filename.startswith("rw_"):
            continue
        result_file = open(result_path + result_filename + ".txt", "r")
        NBO = int(result_filename.split("_")[1])
        if NBO != 32:
            continue
        prac_level = int(result_filename.split("_")[2])
        if prac_level != 1:
            continue
        psq_size = int(result_filename.split("_")[3])
        if psq_size != 32:
            continue
        targeted_ref_ratio = int(result_filename.split("_")[4])
        if mitigation in ['QPRAC+Proactive-EA'] and not targeted_ref_ratio == 1:
            continue
        targeted_ref_ratio = int(result_filename.split("_")[4])

        cache_size = result_filename.split("_")[5]
        if (not cache_size.isnumeric() or int(cache_size) not in [1024]):
            continue
        cache_size = int(cache_size)

        workload = "_".join(result_filename.split("_")[6:])

        counter_reads = 0
        counter_writes = 0
        cached_counter_reads = 0
        cached_counter_writes = 0
        num_inst_total = 0
        for line in result_file.readlines():
            if ("qprac_counter_reads" in line):
                counter_reads = int(line.split(" ")[-1])
            if ("qprac_counter_writes" in line):
                counter_writes = int(line.split(" ")[-1])
            if ("qprac_cached_counter_reads" in line):
                cached_counter_reads = int(line.split(" ")[-1])
            if ("qprac_cached_counter_writes" in line):
                cached_counter_writes = int(line.split(" ")[-1])
            if (" insts_recorded_core_0" in line):
                num_inst_total += int(line.split(" ")[-1])
            if (" insts_recorded_core_1" in line):
                num_inst_total += int(line.split(" ")[-1])
            if (" insts_recorded_core_2" in line):
                num_inst_total += int(line.split(" ")[-1])
            if (" insts_recorded_core_3" in line):
                num_inst_total += int(line.split(" ")[-1])
        
        if (num_inst_total == 0):
            print(workload)
            continue

        r_per_1k = ((counter_reads) / num_inst_total) * 1000
        w_per_1k = ((counter_writes) / num_inst_total) * 1000
        cached_r_per_1k = ((cached_counter_reads) / num_inst_total) * 1000
        cached_w_per_1k = ((cached_counter_writes) / num_inst_total) * 1000
        w_per_1k = ((counter_writes) / num_inst_total) * 1000
        rw_per_1k = ((counter_reads + counter_writes) / num_inst_total) * 1000
        cached_rw_per_1k = ((cached_counter_reads + cached_counter_writes) / num_inst_total) * 1000
        
        result_file.close()
        # Create a new DataFrame for the new row
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'Cache_size': ["RW"],
            '1K': [rw_per_1k],
        })
        df = pd.concat([df, new_row], ignore_index=True)
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'Cache_size': ["R"],
            '1K': [r_per_1k],
        })
        df = pd.concat([df, new_row], ignore_index=True)
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'Cache_size': ["W"],
            '1K': [w_per_1k],
        })
        df = pd.concat([df, new_row], ignore_index=True)
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'Cache_size': ["Cached_RW"],
            '1K': [cached_rw_per_1k],
        })
        df = pd.concat([df, new_row], ignore_index=True)
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'Cache_size': ["Cached_R"],
            '1K': [cached_r_per_1k],
        })
        df = pd.concat([df, new_row], ignore_index=True)
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'NBO': [NBO],
            'Cache_size': ["Cached_W"],
            '1K': [cached_w_per_1k],
        })
        df = pd.concat([df, new_row], ignore_index=True)

df_hit = df.pivot(index=['workload', 'NBO'], columns=['Cache_size'], values='1K').reset_index()
for mitigation in ["Cached_RW", "Cached_R", "Cached_W"]:
    df_hit[mitigation] = 1 - (df_hit[mitigation] / df_hit[mitigation[7:]])

for mitigation in ["RW", "R", "W"]:
    df_hit.drop(columns=[mitigation], inplace=True)

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

    for csize in df['Cache_size'].unique():
        for suite_name, workloads in benchmark_suites.items():
            suite_df = df[(df['workload'].isin(workloads)) & (df['Cache_size'] == csize)]
            if not suite_df.empty:
                ameans = {}
                
                # Dynamically calculate geometric means for each mitigation
                for mitigation in mitigation_list:
                    if mitigation in suite_df.columns:  # Ensure the column exists
                        ameans[mitigation] = calculate_arithmetic_mean(suite_df[mitigation])
                
                # Create a new row
                amean_row = {'Cache_size': csize, 'workload': suite_name, **ameans}
                amean_rows.append(amean_row)  # Append to the list

    # Convert list of rows to DataFrame
    amean_df = pd.DataFrame(amean_rows)
    
    return pd.concat([df, amean_df], ignore_index=True)

# Function to add combined geometric means for all workloads in each channel and interface
def add_all_workloads_amean_rows(df):
    amean_rows = []  # List to collect new rows
    
    for csize in df['Cache_size'].unique():
            Channel_interface_df = df[(df['Cache_size'] == csize)]
            amean_values = {}

            # Calculate geometric means for each mitigation in the list
            for mitigation in mitigation_list:
                if mitigation in Channel_interface_df.columns:  # Ensure the column exists
                    amean_values[mitigation] = calculate_arithmetic_mean(Channel_interface_df[mitigation])

            # Create a new row for the combined results
            amean_row = {'Cache_size': csize, 'workload': 'All (57)', **amean_values}
            amean_rows.append(amean_row)  # Append to the list
    
    # Convert list of rows to DataFrame
    amean_df = pd.DataFrame(amean_rows)
    
    return pd.concat([df, amean_df], ignore_index=True)

mitigation_list = ["Cached_RW", "Cached_R", "Cached_W"]
new_column_order = ['workload', 'NBO'] + mitigation_list

geomean_df = add_geomean_rows(df_hit)
geomean_df = add_all_workloads_geomean_rows(geomean_df)
geomean_df = geomean_df[new_column_order]

# Ensure the results/csvs directory exists
csv_dir = '../results/csvs'
os.makedirs(csv_dir, exist_ok=True)

# Save the CSV file
geomean_df.to_csv(os.path.join(csv_dir, 'QPRAC_32_and_1024_RW_1K.csv'), index=False)