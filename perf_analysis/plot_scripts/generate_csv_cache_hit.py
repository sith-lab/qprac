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
        if not result_filename.startswith("32_"):
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
        if mitigation in ["QPRAC+Proactive", 'QPRAC+Proactive-EA'] and not targeted_ref_ratio == 1:
            continue
        targeted_ref_ratio = int(result_filename.split("_")[3])

        cache_size = result_filename.split("_")[4]
        if (not cache_size.isnumeric() or int(cache_size) not in [128, 256, 512, 1024, 2048]):
            continue
        cache_size = int(cache_size)

        workload = "_".join(result_filename.split("_")[5:])

        cache_hits = 0
        cache_misses = 0
        if (PB):
            for line in result_file.readlines():
                if ("qprac_pb_cache_hits" in line):
                    cache_hits = int(line.split(" ")[-1])
                if ("qprac_pb_cache_misses" in line):
                    cache_misses = int(line.split(" ")[-1])
        else:
            for line in result_file.readlines():
                if ("qprac_cache_hits" in line):
                    cache_hits = int(line.split(" ")[-1])
                if ("qprac_cache_misses" in line):
                    cache_misses = int(line.split(" ")[-1])

        cache_hit_rate = 0
        if (cache_hits + cache_misses == 0):
            print(workload)
        else:
            cache_hit_rate = cache_hits / (cache_hits + cache_misses)
        
        result_file.close()
        # Create a new DataFrame for the new row
        new_row = pd.DataFrame({
            'workload': [workload],
            'mitigation': [mitigation],
            'Cache_size': [cache_size],
            'Cache_hitrate': [cache_hit_rate],
        })
        df = pd.concat([df, new_row], ignore_index=True)

df_hit = df.pivot(index=['workload', 'Cache_size'], columns=['mitigation'], values='Cache_hitrate').reset_index()

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

def add_geomean_psq_rows(df):
    geomean_rows = []  # List to collect new rows

    for qsize in df['Cache_size'].unique():
        for suite_name, workloads in benchmark_suites.items():
            suite_df = df[(df['workload'].isin(workloads)) & (df['Cache_size'] == qsize)]
            if not suite_df.empty:
                geomeans = {}
                
                # Dynamically calculate geometric means for each mitigation
                for mitigation in mitigation_list:
                    if mitigation in suite_df.columns:  # Ensure the column exists
                        geomeans[mitigation] = calculate_geometric_mean(suite_df[mitigation])
                
                # Create a new row
                geomean_row = {'Cache_size': qsize, 'workload': suite_name, **geomeans}
                geomean_rows.append(geomean_row)  # Append to the list

    # Convert list of rows to DataFrame
    geomean_df = pd.DataFrame(geomean_rows)
    
    return pd.concat([df, geomean_df], ignore_index=True)

def add_all_workloads_geomean_psq_rows(df):
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

# Function to add combined geometric means for all workloads in each channel and interface
def add_all_workloads_geomean_psq_rows(df):
    geomean_rows = []  # List to collect new rows
    
    for qsize in df['Cache_size'].unique():
            Channel_interface_df = df[(df['Cache_size'] == qsize)]
            geomean_values = {}

            # Calculate geometric means for each mitigation in the list
            for mitigation in mitigation_list:
                if mitigation in Channel_interface_df.columns:  # Ensure the column exists
                    geomean_values[mitigation] = calculate_geometric_mean(Channel_interface_df[mitigation])

            # Create a new row for the combined results
            geomean_row = {'Cache_size': qsize, 'workload': 'All (57)', **geomean_values}
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

mitigation_list = ["QPRAC+Proactive-EA"]
new_column_order = ['workload', 'Cache_size'] + mitigation_list

geomean_df = add_geomean_psq_rows(df_hit)
geomean_df = add_all_workloads_geomean_psq_rows(geomean_df)
geomean_df = geomean_df[new_column_order]

# Ensure the results/csvs directory exists
csv_dir = '../results/csvs'
os.makedirs(csv_dir, exist_ok=True)

# Save the CSV file
geomean_df.to_csv(os.path.join(csv_dir, 'QPRAC_128_2048_cache_results_pb.csv'), index=False)