import itertools
import argparse

SECONDS_IN_MINUTE = 60

# Slurm username
SLURM_USERNAME = "$USER" 

# Maximum Slurm jobs
MAX_SLURM_JOBS = 1000 

# Delay between submitting Slurm jobs (while job limit is not reached)
SLURM_SUBMIT_DELAY = 0.1 

# Delay between retrying Slurm job submission (when job limit is reached)
SLURM_RETRY_DELAY = 1 * SECONDS_IN_MINUTE 

# Number of threads used for the personal computer runs
PERSONAL_RUN_THREADS = 80

# Number of instructions the slowest core must execute before the simulation ends
NUM_EXPECTED_INSTS = 500_000_000

# Number of cycles the simulation should run
NUM_MAX_CYCLES = 0

CONTROLLER = "BHDRAMController"
SCHEDULER = "BHScheduler"
NUM_RANKS = 2

# # List of evaluated RowHammer mitigation mechanisms
mitigation_list = ["QPRAC", "QPRAC+Proactive", "QPRAC-Ideal"]

# List of evaluated Back-Off thresholds
NBO_lists = [32]

## PRAC Level: # of RFMs per ABO 
PRAC_levels = [2, 4]
# PRAC_levels = [1, 2, 4]

## PSQ Sizes
psq_sizes = [5]

## Targeted Refresh ratio (once per X tREFI)
targeted_ref_ratios = [1]

params_list = [
    mitigation_list,
    NBO_lists,
    PRAC_levels,
    psq_sizes,
    targeted_ref_ratios
]

PARAM_STR_LIST = [
    "mitigation",
    "NBO",
    "PRAC_level",
    "PSQ_size",
    "Targeted_REF_ratio"
]

def get_multicore_params_list():
    params = list(itertools.product(*params_list))
    return params

def make_stat_str(param_list, delim="_"):
    return delim.join([str(param) for param in param_list])

def add_mitigation(config, mitigation, NBO, PRAC_level, PSQ_size, Targeted_REF_ratio):
    config['Frontend']['inst_window_depth'] = 352
    config['MemorySystem'][CONTROLLER]['RowPolicy']['impl'] = 'ClosedRowPolicy'
    config["MemorySystem"][CONTROLLER]["RowPolicy"]["cap"] = 4
    config['MemorySystem']['DRAM']['org']['rank'] = NUM_RANKS
    config['MemorySystem']['DRAM']['PRAC'] = True
    config['MemorySystem'][CONTROLLER]['impl'] = 'PRACOPTDRAMController'
    config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'PRACScheduler'

    if mitigation == "Baseline":
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
    elif mitigation == "QPRAC-NoOp":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': PSQ_size,
                'targeted_ref_frequency': 0,
                'enable_opportunistic_mitigation': False
            }
        })
    elif mitigation == "QPRAC":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': PSQ_size,
                'targeted_ref_frequency': 0,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC+Proactive":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': PSQ_size,
                'targeted_ref_frequency': Targeted_REF_ratio,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC-Ideal":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': 131072,
                'targeted_ref_frequency': Targeted_REF_ratio,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC+1Proactive_per_1tREFI":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': PSQ_size,
                'targeted_ref_frequency': 1,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC+1Proactive_per_2tREFI":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': PSQ_size,
                'targeted_ref_frequency': 2,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC+1Proactive_per_4tREFI":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': PRAC_level,
                'abo_recovery_refs': PRAC_level,
                'abo_act_ns': 180,
                'abo_threshold': NBO,
                'psq_size': PSQ_size,
                'targeted_ref_frequency': 4,
                'enable_opportunistic_mitigation': True
            }
        })
        
if __name__ == "__main__":
    multicore_params = get_multicore_params_list()
    print(multicore_params)