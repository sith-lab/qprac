import sys
import heapq

# Max Heap
class MaxElem:
    def __init__(self, tup: tuple[int, int]):
        self.tup = tup

    def __lt__(self, other):
        return self.tup[0] > other.tup[0] or (self.tup[0] == other.tup[0] and self.tup[1] < other.tup[1])

    def __str__(self):
        return f"(row: {self.tup[1]}, ACT: {self.tup[0]})"
    
    def __repr__(self):
        return f"(row: {self.tup[1]}, ACT: {self.tup[0]})"

def inc_pq_elem(pq, idx):
    tuple_idx = [i for i in range(len(pq)) if pq[i].tup[1] == idx][0]
    it_tup = pq[tuple_idx].tup
    pq[tuple_idx] = MaxElem((it_tup[0] + 1, it_tup[1]))

def dump_pq(pq, record):
    for elem in pq:
        ref_tup = elem.tup
        record.append(MaxElem(ref_tup))

# Needs variables: MIN_WAVE_LEN, MAX_WAVE_LEN, ABO_ACT, ABO_Delay, N_BO
MIN_WAVE_LEN = int(sys.argv[1])
MAX_WAVE_LEN = int(sys.argv[2]) # We sweep all the length in here to find max disturbance
ABO_ACT = int(sys.argv[3])
ABO_DELAY = int(sys.argv[4])
N_BO = int(sys.argv[5])
TREFW = 32000000
max_config = None
pq_full = []
it_full = []
for i in range(MAX_WAVE_LEN):
    pq_full.append(MaxElem((N_BO-1, i)))
    it_full.append(i)

for wave_len in range(MIN_WAVE_LEN, MAX_WAVE_LEN):

    # Generate the wave pattern, PQ {id, count} and List {id}
    record_list = []
    it_pointer = 0
    total_time = 8192 * 295
    it_list = it_full[:wave_len]
    pq = pq_full[:wave_len]
    heapq.heapify(pq)
    
    inc_pq_elem(pq, it_list[it_pointer])
    it_pointer += 1
    it_pointer %= len(pq)

    # 3. Runs for loop until List is empty
    u = 0
    while len(pq) > 0:
        u += 1
        # Continue for ABO_ACT
        for _ in range(ABO_ACT):
            #print(f"ABO_ACT: {it_list[it_pointer]}")
            inc_pq_elem(pq, it_list[it_pointer])
            it_pointer += 1
            it_pointer %= len(pq)
        heapq.heapify(pq)
        total_time += 180
        if (total_time > TREFW):
            dump_pq(pq, record_list)
            break

        for _ in range(ABO_DELAY):
            
            # REF, remove from List the highest id and add it to the record
            ref_tup = heapq.heappop(pq).tup
            #print(f"REF: {ref_tup[1]}")
            record_list.append(MaxElem(ref_tup))
            if len(pq) == 0:
                break

            # If less than it_pointer, we will move left as an element disappeared.
            # we are pointing to the wrong element
            # Otherwise, it_pointer remain unchanged unless it_pointer is the last 
            # element and it_pointer is the one removed.
            tup_it_index = it_list.index(ref_tup[1])
            it_list.remove(ref_tup[1])
            if tup_it_index < it_pointer:
                it_pointer -= 1
            else:
                it_pointer %= len(pq)
        total_time += 350 * 4    
        if (total_time > TREFW):
            dump_pq(pq, record_list)
            break

        # Continue for ABO_Delay
        if len(pq) > 0:
            for _ in range(ABO_DELAY):
                #print(f"ABO_DELAY: {it_list[it_pointer]}")
                inc_pq_elem(pq, it_list[it_pointer])
                it_pointer += 1
                it_pointer %= len(pq)
        total_time += 52 * ABO_DELAY
        if (total_time > TREFW):
            dump_pq(pq, record_list)
            break
    heapq.heapify(record_list)
    if max_config == None or max_config[0] < record_list[0].tup[0]:
        max_config = (record_list[0].tup[0], wave_len)
    print(record_list[0].tup[0], wave_len, u, total_time)
print(max_config[0], max_config[1])

