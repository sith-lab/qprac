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
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/mman.h>

// Refresh Interval in Milliseconds
#define MAX_ACT 559262

//TREFI INTERVALS
#define TREFI_INT 8192

//TREFI MITIGATION INTERVALS
#define TREFI_MIT_FREQ 1

// Acts per TREFI
#define ACTS_PER_TREFI 69

//Number of Rows in a Bank
#define ROWS 65536

//Group Size -- 64K for now
#define GSIZE 65530

//#define GSIZE 16000

//DEBUG ENABLE
#define DENABLE 0

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
    std::vector<Entry> entry_list; // List to enable random access
    size_t max_size; // Maximum size of the priority queue

public:
    PriorityQueueNoDuplicates(size_t maxSize) : max_size(maxSize) {}

    // Add or update the element in the priority queue
    void push(int rowID, int count) {
        auto it = row_to_count.find(rowID);
        if (it != row_to_count.end()) {
            // RowID is already present, update its count
            Entry oldEntry = {it->second, rowID};
            pq.erase(oldEntry);
        }
        row_to_count[rowID] = count;
        Entry newEntry = {count, rowID};
        pq.insert(newEntry);

        // Add to entry list for random access
        entry_list.push_back(newEntry);

        // Evict the lowest count entry if the queue exceeds the maximum size
        if (pq.size() > max_size) {
            auto lowest = --pq.end();
            row_to_count.erase(lowest->rowID);
            pq.erase(lowest);

            // Remove the evicted entry from the entry list
            entry_list.erase(std::remove_if(entry_list.begin(), entry_list.end(), [&](const Entry& e) { return e.rowID == lowest->rowID; }), entry_list.end());
        }
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

            // Remove the popped entry from the entry list
            entry_list.erase(std::remove_if(entry_list.begin(), entry_list.end(),
                                            [&](const Entry& e) { return e.rowID == topElem.rowID; }),
                             entry_list.end());
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
        entry_list.clear();
    }

    // Print the contents of the priority queue for debugging
    void printQueue() const {
        for (const auto& entry : pq) {
            std::cout << "RowID: " << entry.rowID << ", Count: " << entry.count << std::endl;
        }
    }

    // Remove a random entry from the priority queue
    int removeRandom() {
        if (!entry_list.empty()) {
            int randomIndex = rand() % entry_list.size();
            Entry randomEntry = entry_list[randomIndex];
            pq.erase(randomEntry);
            row_to_count.erase(randomEntry.rowID);

            // Remove the random entry from the entry list
            entry_list.erase(entry_list.begin() + randomIndex);
            return randomEntry.rowID;
        }
        else{
            return -1;
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
        std::vector<int> max_activation_list;
        PriorityQueueNoDuplicates pq;

    public:
        DRAM(int numRows, int aboAct, int k, int aboDelay, int alert_th, int max_size)
            : pq (max_size), num_rows(numRows), ABO_ACT(aboAct), K(k), ABO_Delay(aboDelay), ALERT_th(alert_th), 
            alert_flag(0), acts_since_alert(aboDelay), global_max_activation(0), activations_serviced(0) {
                row_activation_counters.resize(num_rows, 0);
                max_activation_list.resize(numRows,0);
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

            if(row_activation_counters[rowID] > max_activation_list[rowID]){
                max_activation_list[rowID] = row_activation_counters[rowID];
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

                if(row_activation_counters[rowID] > max_activation_list[rowID]){
                    max_activation_list[rowID] = row_activation_counters[rowID];
                }

                row_activation_counters[rowID] = 0;
                pq.pop();

                if (rowID > 1) {
                    row_activation_counters[rowID - 2]++;

                    pq.push(rowID-2, row_activation_counters[rowID-2]);

                    if(row_activation_counters[rowID-2] > global_max_activation){
                        global_max_activation = row_activation_counters[rowID-2];
                    }

                    if(row_activation_counters[rowID-2] > max_activation_list[rowID-2]){
                        max_activation_list[rowID-2] = row_activation_counters[rowID-2];
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

                    if(row_activation_counters[rowID-1] > max_activation_list[rowID-1]){
                        max_activation_list[rowID-1] = row_activation_counters[rowID-1];
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

                    if(row_activation_counters[rowID+1] > max_activation_list[rowID+1]){
                        max_activation_list[rowID+1] = row_activation_counters[rowID+1];
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

                    if(row_activation_counters[rowID+2] > max_activation_list[rowID+2]){
                        max_activation_list[rowID+2] = row_activation_counters[rowID+2];
                    }

                    if(DENABLE)
                        std::cout << "ALERT-OFF\t" << "RFMID+2 : " << rowID+2 << "\t" << "COUNT : " << row_activation_counters[rowID+2] << std::endl;
                }
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
                max_activation_list[i] = 0;
            }
            acts_since_alert = 0;
            activations_serviced = 0;
            global_max_activation = 0;
        }

        int get_maxact_rows(){
            int counter = 0;
            for(int i = 0; i < num_rows; i++)
            {
                if(max_activation_list[i] > ALERT_th){
                    counter++;
                }
            }
            return counter;
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
        int gsize;
        int num_alerts;
        std::vector<int> groupsize_maxacts;
        std::vector<int> TREFI;
        int* shared_group_list; // Pointer to shared memory for group
        int* shared_alert_list; // Pointer to shared memory for alerts
        int* shared_uniquerow_list; // Pointer to shared memory for unique rows

    public:
        MemoryController(int numRows, int aboAct, int k, int aboDelay, int alert_th, int simACTs, int gsize, int max_size, int* shared_list, int* alert_list, int* unique_list)
            : dram(numRows, aboAct, k, aboDelay, alert_th, max_size), simulation_acts(simACTs), numRFM (k), current_act(0), activations_since_alert(0), gsize(gsize), num_alerts(0), shared_group_list(shared_list), shared_alert_list(alert_list), shared_uniquerow_list(unique_list) {
                activation_list.resize(numRows, -1);
                groupsize_maxacts.resize(gsize, 0);
                TREFI.resize(TREFI_INT, 0);
            }

        void populateActivationList(int gsize) {
            //Modify based on attack. Currently modeling a random activation attack (sub optimal)
            // The group size needs to be varied.
            for (int i = 0; i < gsize; ++i) {
                activation_list[i] = i;
            }
        }

        void populateTREFIList(int interval) {
            //Modify based on attack. Currently modeling a random activation attack (sub optimal)
            // The group size needs to be varied.
            for (int i = 0; i < TREFI_INT; ++i) {
                if(i%interval == 0){
                    TREFI[i] = 1;
                }
                else{
                    TREFI[i] = 0;
                }
            }
        }

        void simulate_process(int process_id, int start, int end) {
            unsigned long long int counter = 0;
            int listsize = 0;
            int rows = end;
            int num_alerts = 0;
            while(rows >= start){
                listsize = 0;
                populateActivationList(rows);
                counter = 0;
                num_alerts = 0;
                populateTREFIList(TREFI_MIT_FREQ);

                for (current_act = 0; current_act < simulation_acts; ++current_act) {
                    if (TREFI[current_act/ACTS_PER_TREFI] == 1){
                        TREFI[current_act/ACTS_PER_TREFI] = 0;
                        int rowID = dram.RFM(); 
                        // Modelling the TREFI mitigation as an RFM
                        // No need to increase the counters as I have already subtracted this time while determining Max Acts
                        if(rowID >= 0){   
                            if (activation_list[rowID] != -1) 
                            {   
                                activation_list[rowID] = -1; 
                                listsize++;
                            }   
                        }

                        if(listsize >= rows){
                            populateActivationList(rows);
                            listsize = 0;
                        }
                    }
                    else if (dram.checkALERT() && activations_since_alert >= dram.ABO_ACT) {
                        for(int i = 0; i < numRFM; i++){
                            int rowID = dram.RFM();
                            if(rowID >= 0)
                            {   
                                if (activation_list[rowID] != -1) 
                                {   
                                    activation_list[rowID] = -1; 
                                    listsize++;
                                }   
                                current_act = current_act + 7;
                            }
                            if(listsize >= rows){
                                populateActivationList(rows);
                                listsize = 0;
                            }
                        }
                        current_act--;
                        dram.clear_alert();
                        activations_since_alert = 0;
                        num_alerts++;
                    } 
                    else {
                        int rowID = 0;
                        if(listsize >= rows){
                            populateActivationList(rows);
                            listsize = 0;
                        }
                        while(activation_list[counter%rows] < 0){
                            counter++;
                        }
                        rowID = activation_list[counter%rows];
                        dram.activate(rowID);
                        counter++;

                        if(dram.checkALERT()){
                            activations_since_alert++;
                        }
                    }
                }
                shared_group_list[rows] = dram.getglobal_max_activation();
                shared_alert_list[rows] = num_alerts;
                shared_uniquerow_list[rows] = dram.get_maxact_rows();
                //std::cout << "GroupSize : " << rows << " NBO : " << dram.getAlertTH() << " PRAC-CONFIG : " << PRACN << " MAXIMUM_ACT : " << dram.getglobal_max_activation() << std::endl;
                activation_list.clear();
                activations_since_alert = 0;
                dram.clear_alert();
                dram.clear_pq();
                dram.clear_rowcounters();
                if(rows > 100){
                    rows--;
                    while(rows%10 != 0){ 
                        rows--;
                    }   
                }   
                else{
                    rows--;
                }
            }
        }

        void simulate(int gsize, int pracn) {
            const int num_processes = sysconf(_SC_NPROCESSORS_ONLN);
            std::vector<pid_t> pids;
            int chunk_size = gsize / num_processes;

            for (int i = 0; i < gsize; ++i) {
                shared_group_list[i] = i;
            }

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
            std::cout << "GroupSize\t" << " NBO\t" << " PRAC-CONFIG\t" << " MAXIMUM_ACT" << " NUM_ALERTS" << " ROWS_ABOVE_NBO" << std::endl;

            for(int i = 1; i < gsize; i++){
                if(i> 100){
                    if(i%10 == 0){ 
                        if(i < gsize){
                            std::cout << i << "\t" << dram.getAlertTH() << "\t" << pracn << "\t" << shared_group_list[i] << "\t" << shared_alert_list[i] << "\t" << shared_uniquerow_list[i] << std::endl;
                        }   
                    }   
                }   
                else{
                    std::cout << i << "\t" << dram.getAlertTH() << "\t" << pracn << "\t" << shared_group_list[i] << "\t" << shared_alert_list[i] << "\t" << shared_uniquerow_list[i] << std::endl;
                }   
            }   
        }
};

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0] << " <NBO> <PRACN> <ABO_Delay> <MAX Q SIZE>" << std::endl;
        return 1;
    }

    int NBO = std::atoi(argv[1]);
    int PRACN = std::atoi(argv[2]);
    int ABO_Delay = std::atoi(argv[3]);
    int max_size = std::atoi(argv[4]);
    srand(42);

    int numRows = ROWS;
    int K = PRACN;
    int ABO_ACT = 3;
    int simACTs = MAX_ACT; // number of acts
    int alert_th = NBO;

    assert(GSIZE < ROWS);
    // Create shared memory for counting the max activations per groupsize
    int* shared_group_list = static_cast<int*>(mmap(NULL, numRows * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

    if (shared_group_list == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        return 1;
    }

    // Create shared memory for counting alerts per groupsize
    int* shared_alert_list = static_cast<int*>(mmap(NULL, numRows * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

    if (shared_alert_list == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        return 1;
    }

    // Create shared memory for counting the number of unique rows above NBO per groupsize
    int* shared_uniquerow_list = static_cast<int*>(mmap(NULL, numRows * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

    if (shared_uniquerow_list == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        return 1;
    }

    MemoryController mc(numRows, ABO_ACT, K, ABO_Delay, alert_th, simACTs, GSIZE, max_size, shared_group_list, shared_alert_list, shared_uniquerow_list);
    mc.simulate(GSIZE,PRACN);
    munmap(shared_group_list, numRows * sizeof(int)); // Unmap shared memory
    munmap(shared_alert_list, numRows * sizeof(int)); // Unmap shared memory
    munmap(shared_uniquerow_list, numRows * sizeof(int)); // Unmap shared memory


    std::cout << "Simulation completed." << std::endl;
    return 0;
}