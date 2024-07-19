# A Secure, Practical PRAC Implementation using Priority Queues.

### 1. Python Code for Evaluating the Security Bounds Using Wave Attack

* Run command: `cd py_wave_attack ; python wave_attack.py <MIN_WAVE_LEN> <MAX_WAVE_LEN> <ABO_ACT> <ABO_Delay> <N_BO>`
* Example: `python wave_attack.py 2000 2001 3 4 1`
* Arguments:
  * MIN_WAVE_LEN = Set of Rows to Start with (minimum)
  * MAX_WAVE_LEN = Set of Rows to Start with (maximum)
  * ABO_ACT      = ACTs allowed during ALERT
  * ABO_Delay    = ACTs allowed after ALERT before next ALERT
  * N_BO         = Mitigation threshold (threshold for raising an ALERT)
    