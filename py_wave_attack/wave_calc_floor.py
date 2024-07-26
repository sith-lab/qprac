import sys
from queue import PriorityQueue
import heapq
import math
ABO_DELAY = int(sys.argv[3])
ABO_ACT = 3
max_act = 0
max_act_row = 0
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    row_num = i
    calc_row_num = row_num
    act = 0
    
    while math.floor(row_num) > ABO_DELAY:
        act += 1
        if ABO_DELAY == 1 and row_num <= 5:
            act += 1
        ref_rows = math.floor(ABO_DELAY * ((row_num - 2) / (ABO_DELAY + ABO_ACT)))
        row_num -= ref_rows
        #print(total_ACT, num_ALERT, calc_row_num)

        # Due to row_num - 2 < 4 meaning ref is 0, we need to adjust the loss
        # row should still be able to refresh 1 more time.
        if ref_rows == 0:
            break
        #print(f"Row: {row_num}, Row Calc: {calc_row_num}")

    print(act + ABO_DELAY + ABO_ACT + 2, i)
    if act > max_act:
        max_act = act
        max_act_row = i
print(max_act + ABO_DELAY + ABO_ACT + 2, max_act_row)