import sys
import threading
import os

TREFW = 32000000
TRC = 52
TRFC = 410
TRFM = 350
REF = 8192
TREFI = 3905
TABO_ACT = 180
ACT_TREFI = (TREFI - TRFC) // TRC

# Needs variables: MIN_WAVE_LEN, MAX_WAVE_LEN, ABO_ACT, ABO_Delay, N_BO
MIN_WAVE_LEN = int(sys.argv[1])
MAX_WAVE_LEN = int(sys.argv[2]) # We sweep all the length in here to find max disturbance
FILE_NAME = sys.argv[3]

def inc_time(time, val):
    prevTREFI = (time + TREFI + TRFC) // TREFI
    time += val

    # If current time + TRFC will be in the next tREFi, it means current time
    # need to be issued a refresh
    if prevTREFI < (time + TREFI + TRFC) // TREFI:
        time += TRFC
    return time

def my_function(ABO_DELAY, file):
    for N_BO in [2 ** size for size in range(0, 9)]:
        for wave_len in range(MIN_WAVE_LEN, MAX_WAVE_LEN):

            # Generate the wave pattern, PQ {id, count} and List {id}
            total_time = 0
            it_num = wave_len
            if (N_BO > 1):
                act = wave_len * (N_BO - 1)
                total_time = TRC * act + (act // ACT_TREFI) * TRFC

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
            file.write(f"{wave_len} {N_BO}\n")
        else:
            file.write(f"{wave_len - 1} {N_BO}\n")
        file.flush()

threads = []
PRACN = [1, 2, 4]
files = [open("R1-1.txt", "w"), open("R1-2.txt", "w"), open("R1-4.txt", "w")]
for i in range(len(PRACN)):  # Create 3 threads
    thread = threading.Thread(target=my_function, args=(PRACN[i], files[i]))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

for file in files:
    file.close()

os.system(f'mv R1-1.txt {FILE_NAME}')
os.system(f'cat R1-2.txt >> {FILE_NAME}')
os.system(f'cat R1-4.txt >> {FILE_NAME}')
os.system('rm R1-2.txt R1-4.txt')