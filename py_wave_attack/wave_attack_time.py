import sys
from queue import PriorityQueue
import heapq

TREFW = 32000000
TRC = 52
TRFC = 295
TRFM = 350
REF = 8192
TREFI = 3905
TABO_ACT = 180
ACT_TREFI = (TREFI - TRFC) // TRC

# Needs variables: MIN_WAVE_LEN, MAX_WAVE_LEN, ABO_ACT, ABO_Delay, N_BO
MIN_WAVE_LEN = int(sys.argv[1])
MAX_WAVE_LEN = int(sys.argv[2]) # We sweep all the length in here to find max disturbance
ABO_ACT = int(sys.argv[3])
ABO_DELAY = int(sys.argv[4])
N_BO = int(sys.argv[5])
IS_SPECIAL_WAVE = bool(sys.argv[6] == "True")

def inc_time(time, val):
    prevTREFI = (time + TREFI + TRFC) // TREFI
    time += val

    # If current time + TRFC will be in the next tREFi, it means current time
    # need to be issued a refresh
    if prevTREFI < (time + TREFI + TRFC) // TREFI:
        time += TRFC
    return time

for N_BO in [2 ** size for size in range(0, 9)]:
    for wave_len in range(MIN_WAVE_LEN, MAX_WAVE_LEN):

        # Generate the wave pattern, PQ {id, count} and List {id}
        total_time = 0
        it_num = wave_len
        if (N_BO > 1):
            act = wave_len * (N_BO - 1)
            total_time = TRC * act + (act // ACT_TREFI) * TRFC
            # for _ in range(wave_len * (N_BO - 1)):
            #     total_time = inc_time(total_time, TRC)
        
        # Minus tREFi period where the wave rows will be refreshed (avoid this period)
        # total_time += 3905 * (wave_len // 8)
        # Setup.
        # Starting from row 2, activate four apart.

        total_time = inc_time(total_time, TRC)
        # Runs for loop until List is empty
        while it_num > 0:

            total_time = inc_time(total_time, TABO_ACT)
            it_num -= ABO_DELAY
            if it_num <= 0:
                break    
            total_time = inc_time(total_time, TRFM * ABO_DELAY)
            total_time = inc_time(total_time, TRC * ABO_DELAY)
        
        if (total_time > TREFW):
            break
    if (wave_len == MAX_WAVE_LEN - 1):
        print(wave_len, N_BO)
    else:
        print(wave_len - 1, N_BO)
    sys.stdout.flush()
