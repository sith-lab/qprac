import sys
from queue import PriorityQueue
import heapq
import math
ABO_DELAY = int(sys.argv[3])
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    row_num = i
    ABO_ACT = 3
    max_ACT = 0
    while math.floor(row_num) > ABO_DELAY:
        max_ACT += 1
        if (math.floor(ABO_DELAY * row_num / (ABO_DELAY + ABO_ACT)) >= 1):
            row_num -= math.floor(ABO_DELAY * row_num / (ABO_DELAY + ABO_ACT))
        else:
            row_num -= ABO_DELAY * row_num / (ABO_DELAY + ABO_ACT)
    print(max_ACT + ABO_DELAY + ABO_ACT + 2, i)
print(max_ACT + ABO_DELAY + ABO_ACT + 2, i)