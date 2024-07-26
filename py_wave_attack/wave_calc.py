import sys
from queue import PriorityQueue
import heapq
import math
ABO_DELAY = int(sys.argv[3])
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    row_num = i
    ABO_ACT = 3
    max_ACT = 0
    # row_num -= ABO_ACT + 1
    # while math.floor(row_num) > ABO_DELAY:
    #     max_ACT += 1
    #     # ref_num = math.floor(ABO_DELAY * row_num / (ABO_DELAY + ABO_ACT))
    #     ref_num = ABO_DELAY *  row_num / (ABO_DELAY + ABO_ACT)
    #     # ref_num = ABO_DELAY * math.ceil(row_num / (ABO_DELAY + ABO_ACT))
        
    #     if (ref_num >= 1):
    #         ref_num = math.floor(ABO_DELAY *  row_num / (ABO_DELAY + ABO_ACT))
    #     else:
    #         print("Hello?")
    #         ref_num = ABO_DELAY * row_num / (ABO_DELAY + ABO_ACT)
    #     row_num -= ref_num
    #     # if ref_num > ABO_DELAY + ABO_ACT and 0 < row_num <= ABO_DELAY:
    #     #     max_ACT += 1
    #     #print(f"Row Left: {row_num}, Row REFed: {ref_num}")
    while math.floor(row_num) > ABO_DELAY:
        max_ACT += 1
        num_ALERT = math.floor(row_num / (ABO_DELAY + ABO_ACT))
        ref_num = num_ALERT * ABO_DELAY
        row_num -= 4 * ref_num + (row_num - ref_num * num_ALERT)
    print(max_ACT + ABO_DELAY + ABO_ACT + 2, i)
print(max_ACT + ABO_DELAY + ABO_ACT + 2, i)