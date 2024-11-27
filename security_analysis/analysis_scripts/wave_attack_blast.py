import sys
import heapq

TREFW = 32000000
TRC = 52
TRFC = 295
TRFM = 350
REF = 8192
TREFI = 3905
TABO_ACT = 180
# We need to keep track of:
#   All rows in queue
#   REF counts as ACT
#   Now stop only when we reach theoretical tREFw
#   Pattern now works around the Blast radius REF. 0 1 A 3 4 5 6 A 8 9

# Max Heap: (count, id, time_step)
class MaxElem:
    def __init__(self, tup: tuple[int, int, int]):
        self.tup = tup
        self.count = tup[0]
        self.id = tup[1]
        self.time_step = tup[2]

    def __lt__(self, other):
        return (
            self.count > other.count
            or (self.count == other.count and self.time_step < other.time_step)
            or (
                self.count == other.count
                and self.time_step == other.time_step
                and self.id < other.id
            )
        )

    def __str__(self):
        return f"(Row: {self.tup[1]}, ACT: {self.tup[0]}, Recency: {self.tup[2]})"

    def __repr__(self):
        return f"(Row: {self.tup[1]}, ACT: {self.tup[0]}, Recency: {self.tup[2]})"

def inc_pq_elem(pq, idx, time_step):
    tuple_idx = [i for i in range(len(pq)) if pq[i].tup[1] == idx][0]
    it_elem = pq[tuple_idx]
    pq[tuple_idx] = MaxElem((it_elem.count + 1, it_elem.id, time_step))

def dump_pq(pq, record_map):
    for elem in pq:
        ref_tup = elem.tup
        if ref_tup[1] not in record_map or ref_tup[0] > record_map[ref_tup[1]]:
            record_map[ref_tup[1]] = ref_tup[0]

# Needs variables: MIN_WAVE_LEN, MAX_WAVE_LEN, ABO_ACT, ABO_Delay, N_BO
MIN_WAVE_LEN = int(sys.argv[1])
MAX_WAVE_LEN = int(sys.argv[2]) # We sweep all the length in here to find max disturbance
ABO_ACT = int(sys.argv[3])
ABO_DELAY = int(sys.argv[4])
N_BO = int(sys.argv[5])
IS_SPECIAL_WAVE = bool(sys.argv[6] == "True")

MAX_SETUP = TREFW / TRC / (N_BO - 1) if N_BO - 1 > 0 else 65537 # We can setup at most this in a tREFw
max_config = None
pq_full = []
it_full = []

def inc_time(time, val):
    prevTREFI = (time + TREFI + TRFC) // TREFI
    time += val

    # If current time + TRFC will be in the next tREFi, it means current time
    # need to be issued a refresh
    if prevTREFI < (time + TREFI + TRFC) // TREFI:
        time += TRFC
    return time

if (IS_SPECIAL_WAVE):
    PIT = int(sys.argv[7])
    for i in range(2, 2 + 16 * PIT, 5):
        it_full.append(i)
    for i in range(2 + 16 * PIT + 2, MAX_WAVE_LEN + 2 + 16 * PIT + 2):
        it_full.append(i)
    for i in range(0, MAX_WAVE_LEN + 2 + 16 * PIT + 2):
        pq_full.append(MaxElem((N_BO-1, i, i)))
else:
    for i in range(0, MAX_WAVE_LEN):
        pq_full.append(MaxElem((N_BO-1, i, i)))
        it_full.append(i)
for wave_len in range(MIN_WAVE_LEN, MAX_WAVE_LEN):

    # Generate the wave pattern, PQ {id, count} and List {id}
    record_map = {}
    it_pointer = 0
    total_time = 0
    if (IS_SPECIAL_WAVE):
        it_list = it_full[:wave_len + 4 * PIT]
        pq = pq_full[:wave_len + MAX_WAVE_LEN + 2 + 16 * PIT + 2]
        time_step = MAX_WAVE_LEN + 2 + 16 * PIT + 2
        for _ in range(wave_len + MAX_WAVE_LEN + 2 + 16 * PIT + 2):
                for _ in range(N_BO - 1):
                    total_time = inc_time(total_time, TRC)
    else:
        it_list = it_full[:wave_len]
        pq = pq_full[:wave_len]
        time_step = MAX_WAVE_LEN
        if (N_BO > 1):
            for _ in range(wave_len):
                for _ in range(N_BO - 1):
                    total_time = inc_time(total_time, TRC)
    
    # Minus tREFi period where the wave rows will be refreshed (avoid this period)
    total_time += 3905 * (wave_len // 8)
    heapq.heapify(pq)
    # Setup.
    # Starting from row 2, activate four apart.

    inc_pq_elem(pq, it_list[it_pointer], time_step)
    time_step += 1
    it_pointer += 1
    it_pointer %= len(it_list)
    total_time = inc_time(total_time, TRC)
    u = 0
    # Runs for loop until List is empty
    while len(it_list) > 0:
        u+=1
        # Continue for ABO_ACT
        for _ in range(ABO_ACT):
            print(f"ABO_ACT: {it_list[it_pointer]}")
            inc_pq_elem(pq, it_list[it_pointer], time_step)
            time_step += 1
            if len(it_list) > ABO_DELAY:
                it_pointer += 1
                it_pointer %= len(it_list)
        heapq.heapify(pq)
        total_time = inc_time(total_time, TABO_ACT)
        # if (total_time > TREFW):
        #     dump_pq(pq, record_list)
        #     break

        for _ in range(ABO_DELAY):
            
            # REF, remove from List the highest id and add it to the record
            ref_elem = heapq.heappop(pq)
            print(f"REF: {ref_elem}")
            if ref_elem.id not in record_map or ref_elem.count > record_map[ref_elem.id]:
                record_map[ref_elem.id] = ref_elem.count
            pq.append(MaxElem((0, ref_elem.id, time_step)))
            time_step += 1
            for i in [-2, -1, 1, 2]:
                if 0 <= ref_elem.id + i < wave_len:
                    inc_pq_elem(pq, ref_elem.id + i, time_step)
                    time_step += 1
            heapq.heapify(pq)
            # If less than it_pointer, we will move left as an element disappeared.
            # we are pointing to the wrong element
            # Otherwise, it_pointer remain unchanged unless it_pointer is the last 
            # element and it_pointer is the one removed.
            try:
                tup_it_index = it_list.index(ref_elem.id)
                it_list.remove(ref_elem.id)
                if len(it_list) == 0:
                    break

                if tup_it_index < it_pointer:
                    it_pointer -= 1
                else:
                    it_pointer %= len(it_list)
            except:
                continue
        
        total_time = inc_time(total_time, TRFM * ABO_DELAY)
        if len(it_list) <= ABO_DELAY:
            max_it = 0
            max_val = 0
            for it in range(len(it_list)):
                for elem in pq:
                    if elem.id == it_list[it] and elem.count > max_val:
                        max_it = it
                        max_val = elem.count
            it_pointer = max_it

        # if (total_time > TREFW):
        #     dump_pq(pq, record_map)
        #     break

        # Continue for ABO_Delay
        if len(it_list) > 0:
            for _ in range(ABO_DELAY):
                print(f"ABO_DELAY: {it_list[it_pointer]}")
                inc_pq_elem(pq, it_list[it_pointer], time_step)
                time_step += 1
                if len(it_list) > ABO_DELAY:
                    it_pointer += 1
                    it_pointer %= len(it_list)
            total_time = inc_time(total_time, TRC * ABO_DELAY)
        # if (total_time > TREFW):
        #     dump_pq(pq, record_map)
        #     break
    key_max = max(zip(record_map.values(), record_map.keys()))[1]
    if max_config == None or max_config[0] < record_map[key_max]:
        max_config = (record_map[key_max], wave_len, total_time)
    print(record_map[key_max], wave_len)
print(max_config[0], max_config[1])
