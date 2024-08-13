import sys
import queue

ABO_DELAY = 4
ABO_ACT = 3
TREFW = 32000000
TRC = 52
TRFC = 410
TRFM = 350
REF = 8192
TREFI = 3905
TABO_ACT = 180

# Do it for different Queue size, 4 8 16 32 64
# Each Queue size with different TRH, 32, 128, 512 2048, 8192
TRH = 256
for QUEUE_SIZE in range(4, 17):
        act_pointer = 0
        agg_act = 0
        total_act = 0
        agg_map = {i: 0 for i in range(QUEUE_SIZE + 1)}
        MAP_SIZE = QUEUE_SIZE + 1

        AVA_ACT = ( TREFW - (REF * TRFC) ) // TRC
        ACT_TREFI = ( TREFI - TRFC ) // TRC
        ACT_PER_ALERT = QUEUE_SIZE + ABO_ACT + ABO_DELAY

        # 1. Assume tREFI after an Alert until we activate another will refresh all victims in left over queue
        # 2. When we start enqueing, skip activation for the tREFI round if ACT per tREFI is lower than the queue.
        while total_act < AVA_ACT:
            if act_pointer == 0 and agg_map[0] % TRH == TRH - 1:
                # If Not enough time for activating all rows in a tREFI, continue to next tREFI
                if ACT_TREFI - total_act % ACT_TREFI < QUEUE_SIZE:
                    total_act += ACT_TREFI - total_act % ACT_TREFI
                    continue 
                # Make Queue Full
                else:
                    total_act += ACT_PER_ALERT
                    for i in range(ACT_PER_ALERT):
                        agg_map[i % MAP_SIZE] += 1
                        if i % MAP_SIZE == QUEUE_SIZE:
                            agg_act += 1
                    act_pointer = ( act_pointer + ACT_PER_ALERT ) % MAP_SIZE
            else:
                total_act += 1
                agg_map[act_pointer] += 1
                if act_pointer == QUEUE_SIZE:
                    agg_act += 1
                act_pointer = (act_pointer + 1) % MAP_SIZE

        print(agg_act)
