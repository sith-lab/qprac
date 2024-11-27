import sys
import math

ABO_DELAY = int(sys.argv[3])
ABO_ACT = 3
max_act = 0
max_act_row = 0
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    row_num = i - ABO_DELAY
    calc_row_num = row_num - (4 - ABO_DELAY)
    act = 0
    
    while math.floor(row_num) > ABO_DELAY:
        act += 1
        num_ALERT = math.ceil(calc_row_num / (ABO_DELAY + ABO_ACT))
        total_ACT = num_ALERT * (ABO_DELAY + ABO_ACT)
        extra_ACT = total_ACT - calc_row_num - ABO_DELAY
        print(total_ACT, num_ALERT, calc_row_num)
        if (extra_ACT < 0):
            extra_ACT = 0
        row_num -= num_ALERT * ABO_DELAY
        calc_row_num = row_num - extra_ACT - 2
            
        # if math.ceil(calc_row_num / (ABO_DELAY + ABO_ACT)) * 4 > :
        if 0 < row_num <= ABO_DELAY and extra_ACT > 0:
            act += 1

        if row_num == 2 and ABO_DELAY == 1 and calc_row_num <= 0:
            break
        print(f"Row: {row_num}, Row Calc: {calc_row_num}")
    print(act + ABO_DELAY + ABO_ACT + 2, i)
    if act > max_act:
        max_act = act
        max_act_row = i
print(max_act + ABO_DELAY + ABO_ACT + 2, max_act_row)