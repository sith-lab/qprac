import os

NBOS = [16, 32, 64, 128]
ACT = 52
Q_SIZE = 4
TREFI = 3900
TRFC = 410

# Config variable parameters
RFM = {"RFM_ab": 350, "RFM_ab + PRO": 350, "RFM_sb + PRO": 300, "RFM_pb + PRO": 300}

# How many banks are stalled in a RFM.
BANK_NUMS = {"RFM_ab": 32, "RFM_ab + PRO": 32, "RFM_sb + PRO": 8, "RFM_pb + PRO": 1}
ATTACK_GROUP = 100

# RFM_ab
def handle_RFM_ab():
    effective_attack_group = (ATTACK_GROUP - Q_SIZE) # Q_SIZE are removed in first PRAC-4 mitigation
    num_RFM = BANK_NUMS["RFM_ab"] * effective_attack_group + Q_SIZE # + Q_SIZE from first PRAC-4 RFMs.
    time_wasted = RFM["RFM_ab"] * num_RFM
    for NBO in NBOS:
        time_setup = ACT * NBO * ATTACK_GROUP
        print(round(time_wasted / (time_wasted + time_setup) * 100, 2))

def handle_RFM_ab_PRO():
    for NBO in NBOS[:2]:
        time_setup = ACT * NBO * ATTACK_GROUP
        ref_during_setup = time_setup // (TREFI - TRFC)
        effective_attack_group = ATTACK_GROUP - ref_during_setup - Q_SIZE
        num_RFM = BANK_NUMS["RFM_ab + PRO"] * effective_attack_group + Q_SIZE # + Q_SIZE from first PRAC-4 RFMs.
        time_wasted = RFM["RFM_ab + PRO"] * num_RFM
        print(round(time_wasted / (time_wasted + time_setup) * 100, 2))

    # When NBO = 64, larger attack group size have diminishing returns. We have
    # enough time to create 1 attacker per TREFI. We thus simplify our calculation
    # to: create attacker one at a time and each waste an RFM.
    time_wasted = RFM["RFM_ab + PRO"]
    time_setup = ACT * NBOS[2]
    print(round(time_wasted / (time_wasted + time_setup) * 100, 2))

    # 0 RFM as we cannot generate an attacker before TREFI
    print(0)
    

def handle_RFM_sb_PRO():
    for NBO in NBOS[:2]:
        time_setup = ACT * NBO * ATTACK_GROUP
        ref_during_setup = time_setup // (TREFI - TRFC)
        effective_attack_group = ATTACK_GROUP - ref_during_setup - Q_SIZE
        num_RFM = BANK_NUMS["RFM_sb + PRO"] * effective_attack_group + Q_SIZE # + Q_SIZE from first PRAC-4 RFMs.
        time_wasted = RFM["RFM_sb + PRO"] * num_RFM
        print(round(time_wasted / (time_wasted + time_setup) * 100, 2))

    # When NBO = 64, larger attack group size have diminishing returns. We have
    # enough time to create 1 attacker per TREFI. We thus simplify our calculation
    # to: create attacker one at a time and each waste an RFM.
    time_wasted = RFM["RFM_sb + PRO"]
    time_setup = ACT * NBOS[2]
    print(round(time_wasted / (time_wasted + time_setup) * 100, 2))

    # 0 RFM as we cannot generate an attacker before TREFI
    print(0)

def handle_RFM_pb_PRO():
    for NBO in NBOS[:3]:
        # Every bank is on their own, meaning we no longer have the benefit of
        # blocking more bank with RFM. We can simply use the simplified calculation
        time_wasted = RFM["RFM_pb + PRO"]
        time_setup = ACT * NBO
        print(round(time_wasted / (time_wasted + time_setup) * 100, 2))
    
    # 0 RFM as we cannot generate an attacker before TREFI
    print(0)

handle_RFM_ab()
handle_RFM_ab_PRO()
handle_RFM_sb_PRO()
handle_RFM_pb_PRO()