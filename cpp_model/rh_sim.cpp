#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>

class DRAM {
public:
    int num_rows;
    int ABO_ACT;
    int ABO_Delay;
    int K; // Number of RFMs to expect

private:
    int ALERT_th;
    int alert_flag;
    int acts_since_alert;
    int activations_serviced;
  std::vector<int> row_activation_counters; // probably be a heap  or a priority queue.

public:
  DRAM(int numRows, int aboAct, int k, int aboDelay, int alert_th)
      : num_rows(numRows), ABO_ACT(aboAct), K(k), ABO_Delay(aboDelay), ALERT_th(alert_th), 
	alert_flag(0), acts_since_alert(aboDelay), activations_serviced(0) {
        row_activation_counters.resize(num_rows, 0);
    }

    void activate(int rowID) {
      	// TODO: Throw Error if activate called when ABO_ACT limit is crossed by activations after ALERT was asserted high.      
      
        row_activation_counters[rowID]++;

	// Set Alert Flag
        if ( (row_activation_counters[rowID] >= ALERT_th) \
	     && (acts_since_alert >= ABO_Delay)
	     ) {
            alert_flag = 1;
        }

	
        activations_serviced++;
	acts_since_alert++;
    }

    bool checkALERT() {
        return alert_flag;
    }

  // TODO: Optimize to use heap/priority queue.
    void RFM() {     
        std::vector<int> sorted_row_ids(num_rows);
        for (int i = 0; i < num_rows; ++i) {
            sorted_row_ids[i] = i;
        }

        std::sort(sorted_row_ids.begin(), sorted_row_ids.end(), [&](int a, int b) {
            return row_activation_counters[a] > row_activation_counters[b];
        });

        for (int i = 0; i < K; ++i) {	  
            int rowID = sorted_row_ids[i];

	    //TODO: Check if this is the maximum activation count for this Row so far, if so, store in a list.
            row_activation_counters[rowID] = 0;

	    // Assumes BR = 2.
	    if (rowID > 1) row_activation_counters[rowID - 2]++;
            if (rowID > 0) row_activation_counters[rowID - 1]++;
            if (rowID < num_rows - 1) row_activation_counters[rowID + 1]++;
	    if (rowID < num_rows - 2) row_activation_counters[rowID + 2]++;
        }

        alert_flag = 0;
        acts_since_alert = 0;
    }

    int getActivationsServiced() const {
        return activations_serviced;
    }
};

class MemoryController {
private:
    DRAM dram;
    std::vector<int> activation_list;
    int simulation_acts;
    int current_act;
    int activations_since_alert;

public:
  MemoryController(int numRows, int aboAct, int k, int aboDelay, int alert_th, int simACTs)
    : dram(numRows, aboAct, k, aboDelay, alert_th), simulation_acts(simACTs), current_act(0), activations_since_alert(0) {
        populateActivationList();
    }

    void populateActivationList() {

      //Modify based on attack. Currently modeling a random activation attack (sub optimal)
        for (int i = 0; i < simulation_acts; ++i) {
            activation_list.push_back(rand() % dram.num_rows);
        }
    }

    void simulate() {
        for (current_act = 0; current_act < simulation_acts; ++current_act) {
	  // send RFM
            if (dram.checkALERT() && activations_since_alert >= dram.ABO_ACT) {
	        dram.RFM();
                activations_since_alert = 0;
		current_act = current_act + dram.K*5;
            } else {
                int rowID = activation_list[current_act];
                dram.activate(rowID);

		if(dram.checkALERT())
		  activations_since_alert++;
            }
        }
    }
};

int main() {
    srand(42);

    int numRows = 64*1024;
    int K = 4;
    int ABO_ACT = 3;
    int ABO_Delay = K;
    int simACTs = 800000; // number of acts
    int alert_th = 1;
      
    MemoryController mc(numRows, ABO_ACT, K, ABO_Delay, alert_th, simACTs);
    mc.simulate();

    // TODO: Print Max-ACT for top 10 rows, and across all rows.
    
    
    std::cout << "Simulation completed." << std::endl;
    return 0;
}
