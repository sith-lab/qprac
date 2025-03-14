import itertools
import argparse
import os

SECONDS_IN_MINUTE = 60

# Slurm username
SLURM_USERNAME = "$USER" 

# Maximum Slurm jobs (default: 500)
MAX_SLURM_JOBS = int(os.getenv('MAX_SLURM_JOBS', 500))

# Delay between submitting Slurm jobs (while job limit is not reached)
SLURM_SUBMIT_DELAY = 0.1 

# Delay between retrying Slurm job submission (when job limit is reached)
SLURM_RETRY_DELAY = 1 * SECONDS_IN_MINUTE 

# Number of threads used for the personal computer runs (default: 40)
PERSONAL_RUN_THREADS = int(os.getenv('PERSONAL_RUN_THREADS', 40))

# Number of instructions the slowest core must execute before the simulation ends
NUM_EXPECTED_INSTS = 500_000_000

# Number of cycles the simulation should run
NUM_MAX_CYCLES = 0

CONTROLLER = "BHDRAMController"
SCHEDULER = "BHScheduler"
NUM_RANKS = 2

# # List of evaluated RowHammer mitigation mechanisms
mitigation_list = ["RFMsb-1", "RFMsb-2", "RFMsb-5", "RFMsb-10", 'RFMsb-17', "RFMsb-22", 'RFMsb-43', "RFMsb-45", "QPRAC-64", "QPRAC-128", "QPRAC-256", 'QPRAC-512', 'QPRAC-1024']


params_list = [
    mitigation_list
]

PARAM_STR_LIST = [
    "mitigation"
]

def get_multicore_params_list():
    return params_list[0]

def add_mitigation(config, mitigation):
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
    elif mitigation == "QPRAC-64":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': 1,
                'abo_recovery_refs': 1,
                'abo_act_ns': 180,
                'abo_threshold': 32,
                'psq_size': 5,
                'proactive_mitigation_th': 16,
                'targeted_ref_frequency': 1,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC-128":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': 1,
                'abo_recovery_refs': 1,
                'abo_act_ns': 180,
                'abo_threshold': 100,
                'proactive_mitigation_th': 50,
                'psq_size': 5,
                'targeted_ref_frequency': 1,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC-256":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': 1,
                'abo_recovery_refs': 1,
                'abo_act_ns': 180,
                'abo_threshold': 240,
                'proactive_mitigation_th': 120,
                'psq_size': 5,
                'targeted_ref_frequency': 1,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC-512":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': 1,
                'abo_recovery_refs': 1,
                'abo_act_ns': 180,
                'abo_threshold': 500,
                'proactive_mitigation_th': 250,
                'psq_size': 5,
                'targeted_ref_frequency': 1,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "QPRAC-1024":
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'QPRAC',
                'abo_delay_acts': 1,
                'abo_recovery_refs': 1,
                'abo_act_ns': 180,
                'abo_threshold': 1000,
                'proactive_mitigation_th': 500,
                'psq_size': 5,
                'targeted_ref_frequency': 1,
                'enable_opportunistic_mitigation': True
            }
        })
    elif mitigation == "RFMsb-1":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 1,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-2":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 2,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-5":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 5,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-10":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 10,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-17":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 17,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-22":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 22,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-43":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 43,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
    elif mitigation == "RFMsb-45":
        config['MemorySystem']['DRAM']['PRAC'] = False
        config['MemorySystem'][CONTROLLER][SCHEDULER]['impl'] = 'BHScheduler'
        config['MemorySystem'][CONTROLLER]['impl'] = 'OPTDRAMController'
        config['MemorySystem'][CONTROLLER]['plugins'].append({
            'ControllerPlugin' : {
                'impl': 'BATBasedRFM',
                'bat': 45,
                'rfm_type': 1,
                'enable_early_counter_reset': False,
            }
        })
        
if __name__ == "__main__":
    multicore_params = get_multicore_params_list()
    print(multicore_params)