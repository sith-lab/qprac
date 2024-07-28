#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <queue>
#include <unordered_map>
#include <functional>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// Refresh Interval in Milliseconds
#define MAX_ACT 559262

// Number of Rows in a Bank
#define ROWS 65536

// PRAC Number
#define PRACN 1

// Group Size
//#define GSIZE 32768

#define GSIZE 240

// DEBUG ENABLE
#define DENABLE 0

// NBO
#define NBO 32

// Priority queue with no duplicates
class PriorityQueueNoDuplicates {
    private:
        std::priority_queue<std::pair<int, int>> pq; // max-heap priority queue
        std::unordered_map<int, int> row_to_count; // maps rowID to its count

    public:
        // Add or update the element in the priority queue
        void push(int rowID, int count) {
            if (row_to_count.find(rowID) != row_to_count.end()) {
                // RowID is already present, update its count
                row_to_count[rowID] = count;
            } else {
                // New rowID, insert it
                row_to_count[rowID] = count;
            }
            // Push the updated count and rowID to the priority queue
            pq.push(std::make_pair(count, rowID));
        }

        // Get the top element
        std::pair<int, int> top() {
            while (!pq.empty()) {
                auto topElem = pq.top();
                // Ensure that the top element is consistent with the map
                if (row_to_count[topElem.second] == topElem.first) {
                    return topElem;
                }
                pq.pop(); // Remove outdated top element
            }
            return std::pair<int, int>(-1, -1); // Return a default value if the queue is empty
        }

        // Remove the top element
        void pop() {
            while (!pq.empty()) {
                auto topElem = pq.top();
                pq.pop();
                if (row_to_count[topElem.second] == topElem.first) {
                    row_to_count.erase(topElem.second);
                    break;
                }
            }
        }

        // Check if the priority queue is empty
        bool empty() const {
            return row_to_count.empty();
        }

        // Clear the priority queue and the hash map
        void clear() {
            // Clear the priority queue
            while (!pq.empty()) {
                pq.pop();
            }
            // Clear the hash map
            row_to_count.clear();
        }
};

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
        std::vector<int> row_activation_counters; // just a vector of rows
        PriorityQueueNoDuplicates pq;

    public:
        DRAM(int numRows, int aboAct, int k, int aboDelay, int alert_th)
            : num_rows(numRows), ABO_ACT(aboAct), K(k), ABO_Delay(aboDelay), ALERT_th(alert_th), 
            alert_flag(0), acts_since_alert(aboDelay), activations_serviced(0) {
                row_activation_counters.resize(num_rows, 0);
            }

        void activate(int rowID) {
            // TODO: Throw Error if activate called when ABO_ACT limit is crossed by activations after ALERT was asserted high.
            row_activation_counters[rowID]++;
            pq.push(rowID, row_activation_counters[rowID]);

            // Set Alert Flag
            if ((row_activation_counters[rowID] >= ALERT_th) && (acts_since_alert >= ABO_Delay)) {
                alert_flag = 1;
                if (DENABLE)
                    std::cout << "ALERT-ON\t" << "ROWID : " << rowID << "\t" << "COUNT : " << row_activation_counters[rowID] << std::endl;
            }
            else {
                if (DENABLE)
                    std::cout << "\t\t" << "ROWID : " << rowID << "\t" << "COUNT : " << row_activation_counters[rowID] << std::endl;
            }

            activations_serviced++;
            acts_since_alert++;
        }

        bool checkALERT() {
            return alert_flag;
        }

        // TODO: Optimize to use heap/priority queue.
        int RFM() {
            if (!pq.empty()) {
                auto top = pq.top();
                int rowID = top.second;
                row_activation_counters[rowID] = 0;

                if (rowID > 1) {
                    row_activation_counters[rowID - 2]++;
                    if (DENABLE)
                        std::cout << "\t\t" << "RFMID-2 : " << rowID-2 << "\t" << "COUNT : " << row_activation_counters[rowID-2] << std::endl;
                }
                if (rowID > 0) {
                    row_activation_counters[rowID - 1]++;
                    if (DENABLE)
                        std::cout << "\t\t" << "RFMID-1 : " << rowID-1 << "\t" << "COUNT : " << row_activation_counters[rowID-1] << std::endl;
                }
                if (DENABLE) {
                    std::cout << "\t\t" << "RFMID : " << rowID << "\t" << "COUNT : " << row_activation_counters[rowID] << std::endl;
                }
                if (rowID < num_rows - 1) {
                    row_activation_counters[rowID + 1]++;
                    if (DENABLE)
                        std::cout << "\t\t" << "RFMID+1 : " << rowID+1 << "\t" << "COUNT : " << row_activation_counters[rowID+1] << std::endl;
                }
                if (rowID < num_rows - 2) {
                    row_activation_counters[rowID + 2]++;
                    if (DENABLE)
                        std::cout << "ALERT-OFF\t" << "RFMID+2 : " << rowID+2 << "\t" << "COUNT : " << row_activation_counters[rowID+2] << std::endl;
                }
                pq.pop();
                acts_since_alert = 0;
                return rowID;
            }
            else {
                return -1;
            }
        }

        void clear_alert() {
            alert_flag = 0;
        }

        void clear_pq() {
            pq.clear();
        }

        void clear_rowcounters() {
            for (int i = 0; i < num_rows; i++) {
                row_activation_counters[i] = 0;
            }
            acts_since_alert = 0;
            activations_serviced = 0;
        }

        int getActivationsServiced() const {
            return activations_serviced;
        }

        int getTopRowCount() {
            auto top = pq.top();
            return top.first;
        }

        int getAlertTH() {
            return ALERT_th;
        }
};

class MemoryController {
    private:
        DRAM dram;
        int simulation_acts;
        int current_act;
        int activations_since_alert;
        int numRFM; // Number of RFMs 
        int attackcounter;
        int gsize;
        std::vector<int> groupsize_maxacts;
    public:
        MemoryController(int numRows, int aboAct, int k, int aboDelay, int alert_th, int simACTs, int gsize)
            : dram(numRows, aboAct, k, aboDelay, alert_th), simulation_acts(simACTs), numRFM(k), current_act(0), activations_since_alert(0), attackcounter(0), gsize(gsize) {
                groupsize_maxacts.resize(gsize, 0);
            }

        void simulate_process(int process_id, int start, int end) {
            unsigned long long int counter = 0;
            unsigned long long int pool = end;
            int local_activations_since_alert = 0;
            std::vector<int> activation_list;
            for (int i = 0; i < pool; ++i) {
                activation_list.push_back(i);
            }
            std::cout << "Simulation Started\n";
            while (pool >= start) {
                counter = 0;
                for (current_act = 0; current_act < simulation_acts; ++current_act) {
                    // send RFM
                    if (dram.checkALERT() && local_activations_since_alert >= dram.ABO_ACT) {
                        for (int i = 0; i < numRFM; i++) {
                            int rowID = dram.RFM();
                            if (rowID >= 0) {
                                auto it = std::find(activation_list.begin(), activation_list.end(), rowID);
                                if (it != activation_list.end()) {
                                    activation_list.erase(it);
                                }
                                current_act = current_act + 5;
                            }
                            if (activation_list.size() == 0) {
                                for (int i = 0; i < pool; ++i) {
                                    activation_list.push_back(i);
                                }
                            }
                        }
                        dram.clear_alert();
                        local_activations_since_alert = 0;
                    }
                    else {
                        int listsize = activation_list.size();
                        if (listsize == 0) {
                            for (int i = 0; i < pool; ++i) {
                                activation_list.push_back(i);
                            }
                            listsize = activation_list.size();
                        }
                        int rowID = activation_list[counter % listsize];
                        dram.activate(rowID);
                        counter++;
                        if (dram.checkALERT()) {
                            local_activations_since_alert++;
                        }
                    }
                }
                groupsize_maxacts[pool] = dram.getTopRowCount();
                //std::cout << "Process " << process_id << " - GroupSize : " << pool << " NBO : " << dram.getAlertTH() << " PRAC-CONFIG : " << PRACN << " MAXIMUM_ACT : " << dram.getTopRowCount() << std::endl;
                activation_list.clear();
                local_activations_since_alert = 0;
                if(pool){
                    pool--;
                }
                dram.clear_alert();
                dram.clear_pq();
                dram.clear_rowcounters();
            }
        }

        void simulate() {
            const int num_processes = sysconf(_SC_NPROCESSORS_ONLN);
            std::vector<pid_t> pids;
            int chunk_size = gsize / num_processes;

            for (int i = 0; i < num_processes; ++i) {
                pid_t pid = fork();
                if (pid == 0) {
                    int start = i * chunk_size;
                    int end = (i == num_processes - 1) ? gsize : (i + 1) * chunk_size;
                    simulate_process(i, start, end);
                    exit(0);
                }
                else {
                    pids.push_back(pid);
                }
            }

            for (auto& pid : pids) {
                waitpid(pid, nullptr, 0);
            }
            for(int i = 0; i < gsize; i++){
                std::cout << "GroupSize : " << i << " NBO : " << dram.getAlertTH() << " PRAC-CONFIG : " << PRACN << " MAXIMUM_ACT : " << groupsize_maxacts[i] << std::endl;
            }
        }
};

int main() {
    srand(42);

    int numRows = ROWS;
    int K = PRACN;
    int ABO_ACT = 3;
    int ABO_Delay = K;
    int simACTs = MAX_ACT; // number of acts
    int alert_th = NBO;

    MemoryController mc(numRows, ABO_ACT, K, ABO_Delay, alert_th, simACTs, GSIZE);
    mc.simulate();

    std::cout << "Simulation completed." << std::endl;
    return 0;
}
