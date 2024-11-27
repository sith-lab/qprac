import sys
import queue
import copy
ABO_DELAY = 4
ABO_ACT = 3
TREFW = 32000000
TRC = 52
TRFC = 410
TRFM = 350
REF = 8192
TREFI = 3905
TABO_ACT = 180
AVA_ACT = ( TREFW - (REF * TRFC) ) // TRC
ACT_TREFI = ( TREFI - TRFC ) // TRC
ACT_ALERT = (TABO_ACT + TRFM + TRC) // TRC
NBO = int(sys.argv[1])

for GROUP_SIZE in range(1, 2):
    act_pointer = 0
    total_act = 0
    total_alert_act = 0
    total_num_alert = 0
    alert = False
    while total_act < AVA_ACT:
        # 1. activate row in group if group depleted to NBO-1
        # 2. trigger ABO on one element of the group
        # 3. trigger next ABO once ALERT is done
        
        # activations to bring GROUP_SIZE to NBO - 1
        group_act = (NBO - 1) * GROUP_SIZE
        total_act += group_act
        num_alert = GROUP_SIZE - group_act // ACT_TREFI

        # We do nothing during ABO_ACT?
        total_act += num_alert * ACT_ALERT
        total_alert_act += num_alert * ACT_ALERT
        total_num_alert += num_alert
    print(total_alert_act, total_num_alert)
        




    

