#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <queue>
#include <unordered_map>
#include <functional>
#include <assert.h>
#include <set>

// Refresh Interval in Milliseconds
#define MAX_ACT 559262

//Number of Rows in a Bank
#define ROWS 65536

//PRAC Number
#define PRACN 1

//Group Size
#define GSIZE 3

//#define GSIZE 16000

//DEBUG ENABLE
#define DENABLE 0

//NBO
#define NBO 32

// Custom comparator for the set to behave like a max-heap
struct Entry {
    int count;
    int rowID;

    bool operator<(const Entry& other) const {
        if (count != other.count) {
            return count > other.count; // Higher counts first
        }
        return rowID < other.rowID; // If counts are the same, compare rowID
    }
};

class PriorityQueueNoDuplicates {
    private:
        std::set<Entry> pq; // Use set to maintain unique entries with order
        std::unordered_map<int, int> row_to_count; // Maps rowID to its count

    public:
        // Add or update the element in the priority queue
        void push(int rowID, int count) {
    	    std::cout << "ROWID : " << rowID << std::endl;
            auto it = row_to_count.find(rowID);
            if (it != row_to_count.end()) {
                // RowID is already present, update its count
                Entry oldEntry = {it->second, rowID};
                pq.erase(oldEntry);
            }
            row_to_count[rowID] = count;
            Entry newEntry = {count, rowID};
            pq.insert(newEntry);
        }

        // Get the top element
        std::pair<int, int> top() const {
            if (!pq.empty()) {
                const auto& topElem = *pq.begin();
                return std::pair<int, int>(topElem.count, topElem.rowID);
            }
            return std::pair<int, int>(-1, -1); // Return a default value if the queue is empty
        }

        // Remove the top element
        void pop() {
            if (!pq.empty()) {
                const auto& topElem = *pq.begin();
                pq.erase(topElem);
                row_to_count.erase(topElem.rowID);
            }
        }

        // Check if the priority queue is empty
        bool empty() const {
            return pq.empty();
        }

        // Clear the priority queue and the hash map
        void clear() {
            pq.clear();
            row_to_count.clear();
        }

        // Print the contents of the priority queue for debugging
        void printQueue() const {
            for (const auto& entry : pq) {
                std::cout << "RowID: " << entry.rowID << ", Count: " << entry.count << std::endl;
            }
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
        int global_max_activation;
        std::vector<int> row_activation_counters; // just a vector of rows
        PriorityQueueNoDuplicates pq;

    public:
        DRAM(int numRows, int aboAct, int k, int aboDelay, int alert_th)
            : num_rows(numRows), ABO_ACT(aboAct), K(k), ABO_Delay(aboDelay), ALERT_th(alert_th), 
            alert_flag(0), acts_since_alert(aboDelay), global_max_activation(0), activations_serviced(0) {
                row_activation_counters.resize(num_rows, 0);
            }

        void activate(int rowID) {
            // TODO: Throw Error if activate called when ABO_ACT limit is crossed by activations after ALERT was asserted high.
            row_activation_counters[rowID]++;
            pq.push(rowID, row_activation_counters[rowID]);

            // Set Alert Flag
            if ( (row_activation_counters[rowID] >= ALERT_th) && (acts_since_alert >= ABO_Delay)) {
                alert_flag = 1;
                if(DENABLE)
                    std::cout << "ALERT-ON\t" << "ROWID : " << rowID << "\t" << "COUNT : " << row_activation_counters[rowID] << std::endl;
            }
            else{
                if(DENABLE)
                    std::cout << "\t\t" << "ROWID : " << rowID << "\t" << "COUNT : " << row_activation_counters[rowID] << std::endl;
            }

            if(row_activation_counters[rowID] > global_max_activation){
                global_max_activation = row_activation_counters[rowID];
            }
            activations_serviced++;
            acts_since_alert++;
        }

        bool checkALERT() {
            return alert_flag;
        }

        int RFM() {
            if (!pq.empty()){
                auto top = pq.top();
                int rowID = top.second;

                if(row_activation_counters[rowID] > global_max_activation){
                    global_max_activation = row_activation_counters[rowID];
                }

                row_activation_counters[rowID] = 0;
                pq.push(rowID, row_activation_counters[rowID]);

                if (rowID > 1) {
                    row_activation_counters[rowID - 2]++;
                    pq.push(rowID-2, row_activation_counters[rowID-2]);

                    if(row_activation_counters[rowID-2] > global_max_activation){
                        global_max_activation = row_activation_counters[rowID-2];
                    }

                    if(DENABLE)
                        std::cout << "\t\t" << "RFMID-2 : " << rowID-2 << "\t" << "COUNT : " << row_activation_counters[rowID-2] << std::endl;
                }
                if (rowID > 0){ 
                    row_activation_counters[rowID - 1]++;
                    pq.push(rowID-1, row_activation_counters[rowID-1]);

                    if(row_activation_counters[rowID-1] > global_max_activation){
                        global_max_activation = row_activation_counters[rowID-1];
                    }

                    if(DENABLE)
                        std::cout << "\t\t" << "RFMID-1 : " << rowID-1 << "\t" << "COUNT : " << row_activation_counters[rowID-1] << std::endl;
                }
                if(DENABLE){
                    std::cout << "\t\t" << "RFMID : " << rowID << "\t" << "COUNT : " << row_activation_counters[rowID] << std::endl;
                }
                if (rowID < num_rows - 1){
                    row_activation_counters[rowID + 1]++;
                    pq.push(rowID+1, row_activation_counters[rowID+1]);

                    if(row_activation_counters[rowID+1] > global_max_activation){
                        global_max_activation = row_activation_counters[rowID+1];
                    }

                    if(DENABLE)
                        std::cout << "\t\t" << "RFMID+1 : " << rowID+1 << "\t" << "COUNT : " << row_activation_counters[rowID+1] << std::endl;
                }
                if (rowID < num_rows - 2){ 
                    row_activation_counters[rowID + 2]++;
                    pq.push(rowID+2, row_activation_counters[rowID+2]);

                    if(row_activation_counters[rowID+2] > global_max_activation){
                        global_max_activation = row_activation_counters[rowID+2];
                    }

                    if(DENABLE)
                        std::cout << "ALERT-OFF\t" << "RFMID+2 : " << rowID+2 << "\t" << "COUNT : " << row_activation_counters[rowID+2] << std::endl;
                }

                acts_since_alert = 0;
                return rowID;
            }
            else{
                return -1;
            }
        }

        void clear_alert(){
            alert_flag = 0;
        }

        void clear_pq(){
            pq.clear();
        }

        void clear_rowcounters(){
            for(int i = 0; i < num_rows; i++)
            {
                row_activation_counters[i] = 0;
            }
            acts_since_alert = 0;
            activations_serviced = 0;
            global_max_activation = 0;
        }

        int getActivationsServiced() const {
            return activations_serviced;
        }

        int getglobal_max_activation(){
            return global_max_activation;
        }

        int getAlertTH(){
            return ALERT_th;
        }
};

class MemoryController {
    private:
        DRAM dram;
        std::vector<int> activation_list;
        int simulation_acts;
        int current_act;
        int activations_since_alert;
        int numRFM; // Number of RFMs 
        int attackcounter;
    public:
        MemoryController(int numRows, int aboAct, int k, int aboDelay, int alert_th, int simACTs)
            : dram(numRows, aboAct, k, aboDelay, alert_th), simulation_acts(simACTs), numRFM (k), current_act(0), activations_since_alert(0), attackcounter (0){
                activation_list.resize(GSIZE, 0);
            }

        void populateActivationList(int gsize) {
            //Modify based on attack. Currently modeling a random activation attack (sub optimal)
            // The group size needs to be varied.
            for (int i = 0; i < GSIZE; ++i) {
                if(i < gsize)
                    activation_list[i] = i;
                else
                    activation_list[i] = -1;
            }
        }

        void simulate(int gsize){
            unsigned long long int counter = 0;
            int listsize = 0;
            while(attackcounter < gsize){
                listsize = 0;
                populateActivationList(gsize-attackcounter);
                counter = 0;
                for (current_act = 0; current_act < simulation_acts; ++current_act) {
                    // send RFM
                    if (dram.checkALERT() && activations_since_alert >= dram.ABO_ACT) {
                        for(int i = 0; i < numRFM; i++){
                            int rowID = dram.RFM();
                            if(rowID >= 0)
                            {   
                                activation_list[rowID] = -1;
                                listsize++;
                                current_act = current_act + 5;
                            }
                            if(listsize == (gsize-attackcounter)){
                                populateActivationList(gsize-attackcounter);
                            }
                        }
                        dram.clear_alert();
                        activations_since_alert = 0;
                    } 
                    else {
                        int rowID = 0;
                        if(listsize == gsize-attackcounter){
                            populateActivationList(gsize-attackcounter);
                            listsize = 0;
                        }
                        while(activation_list[counter] < 0){
                            counter++;
                        }
                        rowID = activation_list[counter];
                        assert(rowID >= 0);

                        dram.activate(rowID);
                        if(counter < (gsize-attackcounter-1)){
                            counter++;
                        }
                        else{
                            counter = 0;
                        }
                        if(dram.checkALERT()){
                            activations_since_alert++;
                        }
                    }
                }
                std::cout << "GroupSize : " << gsize-attackcounter << " NBO : " << dram.getAlertTH() << " PRAC-CONFIG : " << PRACN << " MAXIMUM_ACT : " << dram.getglobal_max_activation() << std::endl;
                activation_list.clear();
                activations_since_alert = 0;
                dram.clear_alert();
                dram.clear_pq();
                dram.clear_rowcounters();
                attackcounter++;
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

    MemoryController mc(numRows, ABO_ACT, K, ABO_Delay, alert_th, simACTs);
    mc.simulate(GSIZE);

    std::cout << "Simulation completed." << std::endl;
    return 0;
}
