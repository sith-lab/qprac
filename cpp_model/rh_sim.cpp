#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>

class DRAM {
private:
    int num_rows;
    int ABO_ACT;
    int ABO_Delay;
    int K; // Number of RFMs to expect
    int ALERT_th;
    int alert_flag;
    int acts_since_alert;
    int activations_serviced;
  std::vector<int> row_activation_counters; // probably be a heap  or a priority queue.

public:
    DRAM(int numRows, int aboAct, int k, int aboDelay)
        : num_rows(numRows), ABO_ACT(aboAct), K(k), ABO_Delay(aboDelay), 
          alert_flag(0), acts_since_alert(0), activations_serviced(0) {
        row_activation_counters.resize(num_rows, 0);
    }

    void activate(int rowID) {
        row_activation_counters[rowID]++;
        if (row_activation_counters[rowID] > ALERT_th) {
            alert_flag = 1;
        }
        activations_serviced++;
    }

    bool checkALERT() {
        return alert_flag;
    }

    void RFM() {
        std::vector<int> row_ids(num_rows);
        for (int i = 0; i < num_rows; ++i) {
            row_ids[i] = i;
        }

        std::sort(row_ids.begin(), row_ids.end(), [&](int a, int b) {
            return row_activation_counters[a] > row_activation_counters[b];
        });

        for (int i = 0; i < K; ++i) {
            int rowID = row_ids[i];
            row_activation_counters[rowID] = 0;
            if (rowID > 0) row_activation_counters[rowID - 1]++;
            if (rowID < num_rows - 1) row_activation_counters[rowID + 1]++;
        }

        alert_flag = 0;
        acts_since_alert = 0;
        activations_serviced = 0;
    }

    int getActivationsServiced() const {
        return activations_serviced;
    }
};

class MemoryController {
private:
    DRAM dram;
    std::vector<int> activation_list;
    int simulation_time;
    int current_time;
    int activations_since_alert;

public:
    MemoryController(int numRows, int aboAct, int k, int aboDelay, int simTime)
        : dram(numRows, aboAct, k, aboDelay), simulation_time(simTime), current_time(0), activations_since_alert(0) {
        populateActivationList();
    }

    void populateActivationList() {
        for (int i = 0; i < simulation_time; ++i) {
            activation_list.push_back(rand() % dram.num_rows);
        }
    }

    void simulate() {
        for (current_time = 0; current_time < simulation_time; ++current_time) {
            if (dram.checkALERT() && activations_since_alert >= dram.ABO_ACT) {
                for (int i = 0; i < dram.K; ++i) {
                    dram.RFM();
                    activations_since_alert += 5;
                }
            } else {
                int rowID = activation_list[current_time];
                dram.activate(rowID);
                activations_since_alert++;
            }
        }
    }
};

int main() {
    srand(42);

    int numRows = 100;
    int ABO_ACT = 1000;
    int K = 5;
    int ABO_Delay = 200;
    int simTime = 800000;

    MemoryController mc(numRows, ABO_ACT, K, ABO_Delay, simTime);
    mc.simulate();

    std::cout << "Simulation completed." << std::endl;
    return 0;
}
