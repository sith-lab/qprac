#include "base/base.h"
#include "dram_controller/controller.h"
#include "dram_controller/plugin.h"
#include "dram_controller/impl/plugin/prac/prac.h"
#include "dram_controller/impl/plugin/device_config/device_config.h"

#include <limits>
#include <vector>
#include <functional>
#include <unordered_map>
#include <unordered_set>
#include <random>
#include <list>

namespace Ramulator {

class QPRAC : public IControllerPlugin, public Implementation, public IPRAC {
    RAMULATOR_REGISTER_IMPLEMENTATION(IControllerPlugin, QPRAC, "QPRAC", "PRAC Inplementation with Priority Service Queue.")

private:
    class PerBankCounters;

private:
    DeviceConfig m_cfg;
    std::vector<QPRAC::PerBankCounters> m_bank_counters;
    std::vector<int> m_same_bank_offsets;

    Clk_t m_clk = 0;

    ABOState m_state = ABOState::NORMAL;
    Clk_t m_abo_recovery_start = std::numeric_limits<Clk_t>::max();

    int m_abo_act_ns = -1;
    int m_abo_recovery_refs = -1;
    int m_abo_delay_acts = -1;
    int m_abo_thresh = -1;

    int m_abo_act_cycles = -1;

    uint32_t m_abo_recov_rem_refs = -1;
    uint32_t m_abo_delay_rem_acts = -1;
    bool m_is_abo_needed = false;

    bool m_debug = false;
    
    uint32_t m_psq_size = 0;
    uint32_t m_enqueuing_th = 0;
    uint32_t m_proactive_mitigation_th = 0;

    // For mitigations under retention refreshes (Targeted Refresh) -- JESD79-5C.01
    uint32_t m_targeted_ref_frequency = 0; // How often do we perform targeted ref? Ex) Once per tREFI

    bool m_enable_opportunistic_mitigation = false; // To study the impact of opportunistic mitigations
    bool m_random_counter_initializeion; // To start simulation with randomly initialized counter

    // Stats 
    uint64_t s_num_recovery = 0; // # of ABOs
    uint64_t s_num_targeted_ref = 0; // # of total Targeted REF

    uint64_t s_psq_len = 0;
    double s_avg_psq_len = 0.0;

    // Stats for energy/power
    uint64_t s_num_total_mitigations = 0;
    double qprac_static_power = 0.380784;  //mW -- Based on Synopsys DC with 45nm Nangate Open Cell Library
    double s_qprac_total_dynamic_energy = 0.0; //nJ
    double s_qprac_total_static_energy = 0.0;  //nJ
    double s_qprac_total_mitigation_energy = 0.0;  //nJ

    // Queue hit rate
    uint64_t s_queue_misses = 0;
    uint64_t s_queue_hits = 0;

    // Counter cache hit rate
    uint64_t s_cache_misses = 0;
    uint64_t s_cache_hits = 0;

    // Counter cache hit rate
    uint64_t s_pb_cache_misses = 0;
    uint64_t s_pb_cache_hits = 0;

    // Counter RW
    uint64_t s_counter_reads = 0;
    uint64_t s_counter_writes = 0;
    uint64_t s_cached_counter_reads = 0;
    uint64_t s_cached_counter_writes = 0;
    uint64_t s_q_counter_reads = 0;
    uint64_t s_q_counter_writes = 0;
    uint64_t s_wb_counter_reads = 0;
    uint64_t s_wb_counter_writes = 0;
    uint64_t s_wb_abo = 0;

    uint64_t s_rwb_counter_reads = 0;
    uint64_t s_rwb_counter_writes = 0;

    uint32_t m_cache_size = 0;
    uint32_t m_cache_way = 0;
    uint32_t m_wb_th = 0;

public:
    void init() override { 
        m_debug = param<bool>("debug").default_val(false);
        m_abo_delay_acts = param<int>("abo_delay_acts").default_val(4);
        m_abo_recovery_refs = param<int>("abo_recovery_refs").default_val(4);
        m_abo_act_ns = param<int>("abo_act_ns").default_val(180);
        m_abo_thresh = param<int>("abo_threshold").default_val(512);

        // For Priority Service Queue configurations
        m_psq_size = param<uint32_t>("psq_size").default_val(5);
        m_enqueuing_th = param<uint32_t>("enqueuing_th").default_val(1);
        m_proactive_mitigation_th = param<uint32_t>("proactive_mitigation_th").default_val(0);
        // For Targeted Refresh
        m_targeted_ref_frequency = param<uint32_t>("targeted_ref_frequency").default_val(1);

        m_cache_size = param<uint32_t>("cache_size").default_val(64);
        m_cache_way = param<uint32_t>("cache_way").default_val(4);

        m_wb_th = param<uint32_t>("wb_th").default_val(16);
    
        m_enable_opportunistic_mitigation = param<bool>("enable_opportunistic_mitigation").default_val(true);
        m_random_counter_initializeion = param<bool>("random_counter_initializeion").default_val(false);
    }

    void setup(IFrontEnd* frontend, IMemorySystem* memory_system) override {
        m_cfg.set_device(cast_parent<IDRAMController>());
        init_dram_params(m_cfg.m_dram);

        m_is_abo_needed = false;
        m_abo_act_cycles = m_abo_act_ns / ((float) m_cfg.m_dram->m_timing_vals("tCK_ps") / 1000.0f);
        register_stat(s_num_targeted_ref).name("num_targeted_ref");
        register_stat(s_num_total_mitigations).name("num_total_mitigations");

        register_stat(s_psq_len).name("psq_len");
        register_stat(s_avg_psq_len).name("avg_psq_len");
        // Stats for power/energy
        register_stat(s_qprac_total_dynamic_energy).name("qprac_dynamic_energy");
        register_stat(s_qprac_total_static_energy).name("qprac_static_energy");
        register_stat(s_qprac_total_mitigation_energy).name("qprac_mitigation_energy");

        register_stat(s_queue_misses).name("qprac_q_misses");
        register_stat(s_queue_hits).name("qprac_q_hits");
        register_stat(s_cache_misses).name("qprac_cache_misses");
        register_stat(s_cache_hits).name("qprac_cache_hits");
        register_stat(s_pb_cache_misses).name("qprac_pb_cache_misses");
        register_stat(s_pb_cache_hits).name("qprac_pb_cache_hits");
        register_stat(s_counter_reads).name("qprac_counter_reads");
        register_stat(s_counter_writes).name("qprac_counter_writes");
        register_stat(s_cached_counter_reads).name("qprac_cached_counter_reads");
        register_stat(s_cached_counter_writes).name("qprac_cached_counter_writes");
        register_stat(s_q_counter_reads).name("qprac_q_counter_reads");
        register_stat(s_q_counter_writes).name("qprac_q_counter_writes");
        register_stat(s_wb_counter_reads).name("qprac_wb_counter_reads");
        register_stat(s_wb_counter_writes).name("qprac_wb_counter_writes");
        register_stat(s_wb_abo).name("qprac_wb_abo");
        register_stat(s_rwb_counter_reads).name("qprac_rwb_counter_reads");
        register_stat(s_rwb_counter_writes).name("qprac_rwb_counter_writes");

        m_bank_counters.reserve(m_cfg.m_num_banks);
        for (int i = 0; i < m_cfg.m_num_banks; i++) {
            m_bank_counters.emplace_back(i, m_cfg, m_is_abo_needed, m_abo_thresh, m_debug, m_psq_size, m_enqueuing_th, m_proactive_mitigation_th, m_targeted_ref_frequency, m_enable_opportunistic_mitigation, s_num_total_mitigations, s_num_targeted_ref, s_qprac_total_dynamic_energy, m_random_counter_initializeion, s_queue_hits, s_queue_misses, s_cache_hits, s_cache_misses, s_pb_cache_hits, s_pb_cache_misses, m_cache_size, m_cache_way, s_counter_reads, s_counter_writes, s_cached_counter_reads, s_cached_counter_writes, s_q_counter_reads, s_q_counter_writes, s_wb_counter_reads, s_wb_counter_writes, s_wb_abo, m_wb_th, s_rwb_counter_reads, s_rwb_counter_writes);
        }

        register_stat(s_num_recovery).name("prac_num_recovery");
    }

    void update(bool request_found, ReqBuffer::iterator& req_it) override {
        m_clk++;
        
        update_state_machine(request_found, *req_it);

        for (size_t i = 0; i < m_cfg.m_num_banks; i++) {
            s_psq_len += m_bank_counters[i].print_psq_size();
        }

        if (!request_found) {
            return;
        }

        auto& req = *req_it;
        auto& req_meta = m_cfg.m_dram->m_command_meta(req.command);
        auto& req_scope = m_cfg.m_dram->m_command_scopes(req.command);

        bool has_bank_wildcard = req.addr_vec[m_cfg.m_bank_level] == -1;
        bool has_bankgroup_wildcard = req.addr_vec[m_cfg.m_bankgroup_level] == -1;
        if (has_bankgroup_wildcard && has_bank_wildcard) { // All BG, All Bank
            int offset = req.addr_vec[m_cfg.m_rank_level] * m_cfg.m_num_banks_per_rank;
            for (int i = 0; i < m_cfg.m_num_banks_per_rank; i++) {
                m_bank_counters[offset + i].on_request(req);
            }
            req.addr_vec[m_cfg.m_bank_level] = -1;
        }
        else if (has_bankgroup_wildcard) { // All BG, Single Bank
            int rank_offset = req.addr_vec[m_cfg.m_rank_level] * m_cfg.m_num_banks_per_rank;
            int bank_offset = req.addr_vec[m_cfg.m_bank_level];
            for (int i = 0; i < m_cfg.m_num_bankgroups; i++) {
                int bg_offset = i * m_cfg.m_num_banks_per_bankgroup;
                m_bank_counters[rank_offset + bg_offset + bank_offset].on_request(req);
            }
        }
        else if (has_bank_wildcard) { // Single BG, All Bank
            int rank_offset = req.addr_vec[m_cfg.m_rank_level] * m_cfg.m_num_banks_per_rank;
            int bg_offset = req.addr_vec[m_cfg.m_bankgroup_level] * m_cfg.m_num_banks_per_bankgroup; 
            for (int i = 0; i < m_cfg.m_num_banks_per_bankgroup; i++) {
                m_bank_counters[rank_offset + bg_offset + i].on_request(req);
            }
        }
        else { // Single BG, Single Bank
            auto flat_bank_id = m_cfg.get_flat_bank_id(req);
            m_bank_counters[flat_bank_id].on_request(req);
        }
    }

    void update_state_machine(bool request_found, const Request& req) {
        std::unordered_map<ABOState, std::string> state_names = {
            {ABOState::NORMAL, "ABOState::NORMAL"},
            {ABOState::PRE_RECOVERY, "ABOState::PRE_RECOVERY"},
            {ABOState::RECOVERY, "ABOState::RECOVERY"},
            {ABOState::DELAY, "ABOState::DELAY"}
        };
        auto cmd_prea = m_cfg.m_dram->m_commands("PREA");
        auto cmd_rfmab = m_cfg.m_dram->m_commands("RFMab");
        auto cmd_rfmsb = m_cfg.m_dram->m_commands("RFMsb");
        auto cmd_act = m_cfg.m_dram->m_commands("ACT");
        auto cur_state = m_state;
        switch(m_state) {
        case ABOState::NORMAL:
            if (m_is_abo_needed) {
                if (m_debug) {
                    std::printf("[PRAC] [%lu] <%s> Asserting ALERT_N.\n", m_clk, state_names[cur_state].c_str());
                }
                m_state = ABOState::PRE_RECOVERY;
                m_abo_recovery_start = m_clk + m_abo_act_cycles;
                s_num_recovery++;
            }
            break;
        case ABOState::PRE_RECOVERY:
            if (request_found && req.command == cmd_prea) {
                if (m_debug) {
                    std::printf("[PRAC] [%lu] <%s> Received PREA.\n", m_clk, state_names[cur_state].c_str());
                }
            }
            if (m_clk == m_abo_recovery_start) {
                m_state = ABOState::RECOVERY;
                m_abo_recovery_start = std::numeric_limits<Clk_t>::max();
                m_abo_recov_rem_refs = m_abo_recovery_refs * m_cfg.m_num_ranks;
            }
            break;
        case ABOState::RECOVERY:
            if (request_found && req.command == cmd_rfmab) {
                m_abo_recov_rem_refs--;
                if (!m_abo_recov_rem_refs) {
                    m_state = ABOState::DELAY;
                    m_abo_delay_rem_acts = m_abo_delay_acts;
                }
            }
            break;
        case ABOState::DELAY:
            if (request_found && req.command == cmd_act) {
                m_abo_delay_rem_acts--;
                if (!m_abo_delay_rem_acts) {
                    m_is_abo_needed = false;
                    for (int i = 0; i < m_cfg.m_num_banks; i++) {
                        m_is_abo_needed |= m_bank_counters[i].is_critical();
                    }
                    m_state = ABOState::NORMAL;
                }
            }
            break;
        }
        if (m_debug && cur_state != m_state) {
            std::printf("[PRAC] [%lu] <%s> -> <%s>\n", m_clk, state_names[cur_state].c_str(), state_names[m_state].c_str());
        }
    }

    Clk_t next_recovery_cycle() override {
        return m_abo_recovery_start;
    }

    int get_num_abo_recovery_refs() override {
        return m_abo_recovery_refs;
    }

    ABOState get_state() override {
        return m_state;
    }

    void finalize() override {
        s_avg_psq_len = (double)s_psq_len / (double)m_clk;
        s_avg_psq_len = s_avg_psq_len / (double)m_cfg.m_num_banks;

        // Calculate the QPRAC energy consumption here
        double VDD = m_cfg.m_dram->m_voltage_vals("VDD");
        double VPP = m_cfg.m_dram->m_voltage_vals("VPP");

        double IDD0 = m_cfg.m_dram->m_current_vals("IDD0");
        double IPP0 = m_cfg.m_dram->m_current_vals("IPP0");

        double IDD2N = m_cfg.m_dram->m_current_vals("IDD2N");
        double IPP2N = m_cfg.m_dram->m_current_vals("IPP2N");

        double IDD3N = m_cfg.m_dram->m_current_vals("IDD3N");
        double IPP3N = m_cfg.m_dram->m_current_vals("IPP3N");

        double tCK_ns = (double) m_cfg.m_dram->m_timing_vals("tCK_ps") / 1000.0;
        double tRAS = (double) m_cfg.m_dram->m_timing_vals("nRAS") * tCK_ns;
        double tRP = (double) m_cfg.m_dram->m_timing_vals("nRP") * tCK_ns;
        double tRC = tRAS + tRP;
        double mitigation_energy = ((((VDD * (IDD0 - IDD3N) + VPP * (IPP0 - IPP3N))) * tRAS)
                                    + ((VDD * (IDD0 - IDD2N) + VPP * (IPP0 - IPP2N)) * tRP)) / 1E3;
        // Each mitigation refresh/reset five rows.
        mitigation_energy = (double)mitigation_energy * 5.0;

        s_qprac_total_static_energy += (double)qprac_static_power * (double)m_clk * tCK_ns * m_cfg.m_num_ranks / 1E3;
        s_qprac_total_mitigation_energy = (double)s_num_total_mitigations * (double)mitigation_energy;
    }

private:
    class PerBankCounters {
    public: 
        PerBankCounters(int bank_id, DeviceConfig& cfg, bool& is_abo_needed, int alert_thresh, bool debug, uint32_t psq_size, uint32_t enqueuing_th, uint32_t proactive_mitigation_th, uint32_t targeted_ref_frequency, bool enable_opportunistic_mitigation, uint64_t& num_total_mitigations, uint64_t& num_targeted_ref, double& qprac_total_dynamic_energy, bool random_counter_initializeion, uint64_t& queue_hits, uint64_t& queue_misses, uint64_t& cache_hits, uint64_t& cache_misses, uint64_t& pb_cache_hits, uint64_t& pb_cache_misses, uint64_t cache_size, uint64_t cache_way, uint64_t& counter_reads, uint64_t& counter_writes, uint64_t& cached_counter_reads, uint64_t& cached_counter_writes, uint64_t& q_counter_reads, uint64_t& q_counter_writes, uint64_t& wb_counter_reads, uint64_t& wb_counter_writes, uint64_t& wb_abo, uint64_t wb_th, uint64_t& rwb_counter_reads, uint64_t& rwb_counter_writes)
        : m_bank_id(bank_id), m_cfg(cfg), m_is_abo_needed(is_abo_needed),
        m_alert_thresh(alert_thresh), m_debug(debug), m_psq_size(psq_size), m_enqueuing_th(enqueuing_th), m_proactive_mitigation_th(proactive_mitigation_th),
        m_targeted_ref_frequency(targeted_ref_frequency), m_enable_opportunistic_mitigation(enable_opportunistic_mitigation), s_num_total_mitigations(num_total_mitigations), 
        s_num_targeted_ref(num_targeted_ref), s_qprac_total_dynamic_energy(qprac_total_dynamic_energy), m_random_counter_initializeion(random_counter_initializeion),
        s_queue_hits(queue_hits), s_queue_misses(queue_misses), s_cache_hits(cache_hits), s_cache_misses(cache_misses), s_pb_cache_hits(pb_cache_hits), s_pb_cache_misses(pb_cache_misses), m_cache_size(cache_size), 
        s_counter_reads(counter_reads), s_counter_writes(counter_writes), s_cached_counter_reads(cached_counter_reads), s_cached_counter_writes(cached_counter_writes),
        s_q_counter_reads(q_counter_reads), s_q_counter_writes(q_counter_writes), s_wb_counter_reads(wb_counter_reads), s_wb_abo(wb_abo),
        s_wb_counter_writes(wb_counter_writes), s_rwb_counter_reads(rwb_counter_reads), s_rwb_counter_writes(rwb_counter_writes){
            init_dram_params(m_cfg.m_dram);
            reset();
            m_pb_counter_cache = Cache(cache_size, 16, cache_way);
            m_writeBuffers = std::vector<WriteBuffer>(16, WriteBuffer(16, wb_th, wb_th / 2));
            m_readBuffers = std::vector<ReadBuffer>(16, ReadBuffer(wb_th / 2));
        }

        ~PerBankCounters() {
            m_counters.clear();
        }

        void on_request(const Request& req) {
            if (m_handlertable.find(req.command) != m_handlertable.end()) {
                m_handlertable[req.command].handler(req);
            }
        }

        void init_dram_params(IDRAM* dram) {
            CommandHandler handlers[] = {
                // TODO: We should process PREs? Doesn't really change the results though.
                {std::string("ACT"), std::bind(&PerBankCounters::process_act, this, std::placeholders::_1)},
                {std::string("RFMab"), std::bind(&PerBankCounters::process_rfm, this, std::placeholders::_1)},
                {std::string("RFMsb"), std::bind(&PerBankCounters::process_rfm, this, std::placeholders::_1)},
                {std::string("REFab"), std::bind(&PerBankCounters::process_targeted_ref, this, std::placeholders::_1)}
            };
            for (auto& h : handlers) {
                if (!dram->m_commands.contains(h.cmd_name)) {
                    std::cout << "[PRAC] Command " << h.cmd_name << "does not exist." << std::endl;
                    exit(0);
                }
                m_handlertable[dram->m_commands(h.cmd_name)] = h;
            }
        }

        void reset() {
            m_counters.clear();
            m_critical_rows.clear();
            m_psq.clear();
        }

        bool is_critical() {
            return m_critical_rows.size() > 0;
        }

        uint64_t print_psq_size(){
            if(m_psq.empty())
                return 0;

            return m_psq.size();
        }

    private:
    class CacheLine {
        public:
            bool valid;
            int tag;
            int counter; // Counter instead of generic data
            int bank_id;
        
            CacheLine() : valid(false), tag(-1), counter(0), bank_id(0) {}
        };
        
        class Set {
        public:
            int ways;
            std::list<std::pair<int, int>> lru_list; // Keeps track of LRU order
            std::unordered_map<std::string, std::list<std::pair<int, int>>::iterator> lru_map; // Tag -> LRU position
            std::vector<CacheLine> lines;
        
            Set(int n) : ways(n), lines(n) {}
        
            int access(int tag, int bank_id = 0) {
                for (int i = 0; i < ways; i++) {
                    if (lines[i].valid && lines[i].tag == tag && lines[i].bank_id == bank_id) {
                        updateLRU(tag, bank_id);
                        return lines[i].counter;
                    }
                }
                return -1; // Indicating cache miss
            }
        
            int insert(int tag, int counter, int bank_id = 0) {
                // If there's an empty spot, use it
                for (int i = 0; i < ways; i++) {
                    if (!lines[i].valid) {
                        lines[i].valid = true;
                        lines[i].tag = tag;
                        lines[i].counter = counter;  // Initialize counter
                        lines[i].bank_id = bank_id;
                        updateLRU(tag, bank_id);
                        return -1;
                    }
                }
        
                // Otherwise, evict the LRU entry
                int evict_tag = lru_list.back().first;
                int evict_bank = lru_list.back().second;
                lru_list.pop_back();
                lru_map.erase(std::to_string(evict_tag) + "_" + std::to_string(evict_bank));
        
                // Replace the evicted entry
                for (int i = 0; i < ways; i++) {
                    if (lines[i].tag == evict_tag && lines[i].bank_id == evict_bank) {
                        lines[i].tag = tag;
                        lines[i].valid = true;
                        lines[i].counter = counter;  // Reset counter
                        lines[i].bank_id = bank_id;
                        break;
                    }
                }
        
                updateLRU(tag, bank_id);
                return tag;
            }
        
        private:
            void updateLRU(int tag, int bank_id) {
                // Remove if already in LRU list
                auto key = std::to_string(tag) + "_" + std::to_string(bank_id);
                if (lru_map.find(key) != lru_map.end()) {
                    lru_list.erase(lru_map[key]);
                }
                // Add to front (most recently used)
                lru_list.push_front({tag, bank_id});
                lru_map[key] = lru_list.begin();
            }
        };
        
        class Cache {
        public:
            int sets, ways;
            std::vector<Set> cacheSets;
            std::hash<int> h;
            std::hash<std::string> hStr;
            
            Cache(){};
            Cache(int cacheSize, int blockSize, int ways)
                : ways(ways) {
                sets = cacheSize / ways;
                cacheSets = std::vector<Set>(sets, Set(ways));
            }
        
            int access(int address, int bank_id = 0) {
                int index = h(address) % sets;  // Index selection from row ID
                int tag = address;                 // Entire row ID acts as tag
        
                int result = cacheSets[index].access(tag, bank_id);
                if (result != -1) {
                    return result;
                } else {
                    return -1; // First access initializes counter to 1
                }
            }
    
            int insert(int address, int counter, int bank_id = 0) {
                int index = h(address) % sets;  // Index selection from row ID
                int tag = address;                 // Entire row ID acts as tag
                
                return cacheSets[index].insert(tag, counter, bank_id);
            }
        };
    
        class WriteBuffer {
        public:
            int size, flush_th, hitflush_th;
            
            std::map<int, int> buffer;
            WriteBuffer(){};
            WriteBuffer(int size, int flush_th, int hitflush_th)
                : size(size), flush_th(flush_th), hitflush_th(hitflush_th) {
                
            }
    
            bool find(int row_addr)
            {
                return buffer.find(row_addr) != buffer.end();
            }
    
            bool isPastThreshold()
            {
                return buffer.size() >= flush_th;
            }

            bool isPastHitFlushThreshold()
            {
                return buffer.size() >= hitflush_th;
            }
    
            /* Return true when past ABO threshold */
            bool insert(int row_addr, int val)
            {
                int p_size = buffer.size();
                buffer[row_addr] = val;
                if (p_size < flush_th && buffer.size() == flush_th)
                    return true;
                return false;
            }
    
            int flush()
            {
                int p_size = buffer.size();
                buffer.clear();
                return p_size;
            }
        };

        class ReadBuffer {
            public:
                int size;
                
                std::vector<int> buffer;
                ReadBuffer(){};
                ReadBuffer(int size)
                    : size(size) {
                    
                }
        
                bool find(int row_addr)
                {
                    return std::find(buffer.begin(), buffer.end(), row_addr) != buffer.end();
                }
        
                bool isFull()
                {
                    return buffer.size() == size;
                }
        
                /* Return true when past ABO threshold */
                void insert(int row_addr)
                {
                    buffer.push_back(row_addr);
                }
        
                int flush()
                {
                    int p_size = buffer.size();
                    buffer.clear();
                    return p_size;
                }
            };

        struct CommandHandler {
            std::string cmd_name;
            std::function<void(const Request&)> handler;
        };

        DeviceConfig& m_cfg;
        bool& m_is_abo_needed;

        // To test impact of counter reset during refreshes.
        std::mt19937 gen;
        std::uniform_int_distribution<int> dist;

        std::unordered_map<int, uint32_t> m_counters;
        std::unordered_map<int, uint32_t> m_critical_rows;
        std::unordered_map<int, CommandHandler> m_handlertable;

        int m_alert_thresh = -1;
        bool m_debug = false;
        int m_bank_id = -1;

        // For PSQ and configuration
        std::unordered_map<int, uint32_t> m_psq;
        uint32_t m_psq_size = 0;
        uint32_t m_enqueuing_th = 0;
        uint32_t m_proactive_mitigation_th = 0;

        bool m_enable_opportunistic_mitigation = true;
        bool m_random_counter_initializeion = false;
        // For Targeted REF
        uint32_t m_targeted_ref_frequency = 0;
        uint64_t m_num_ref = 0;

        // For stats
        uint64_t& s_num_targeted_ref;

        uint64_t& s_queue_hits;
        uint64_t& s_queue_misses;
        uint64_t& s_cache_hits;
        uint64_t& s_cache_misses;

        uint64_t& s_pb_cache_hits;
        uint64_t& s_pb_cache_misses;
        Cache m_pb_counter_cache;

        uint64_t m_cache_size;

        uint64_t& s_counter_reads;
        uint64_t& s_counter_writes;
        
        uint64_t& s_cached_counter_reads;
        uint64_t& s_cached_counter_writes;

        uint64_t& s_q_counter_reads;
        uint64_t& s_q_counter_writes;
        uint64_t& s_wb_counter_reads;
        uint64_t& s_wb_counter_writes;
        uint64_t& s_wb_abo;
        uint64_t& s_rwb_counter_reads;
        uint64_t& s_rwb_counter_writes;

        std::vector<WriteBuffer> m_writeBuffers;
        std::vector<ReadBuffer> m_readBuffers;

        // For power related stats
        uint64_t& s_num_total_mitigations;
        double& s_qprac_total_dynamic_energy;
        double qprac_per_bank_access_energy = 0.000236893; //nJ -- Based on Synopsys DC with 45nm Nangate Open Cell Library

        int tryFlushMaxWB()
        {
            auto maxBuf = std::max_element(m_writeBuffers.begin(), m_writeBuffers.end(), 
                [](WriteBuffer &buf_a, WriteBuffer &buf_b){
                    return buf_a.buffer.size() < buf_b.buffer.size();
                });

            if (maxBuf->isPastHitFlushThreshold())
            {
                maxBuf->flush();
                return std::distance(m_writeBuffers.begin(), maxBuf);
            }
            return -1;
        }

        bool tryFlushRB(int row_addr)
        {
            std::vector<int> rows;
            for(auto const& item: m_readBuffers[getCounterRow(row_addr)].buffer)
                rows.push_back(item);
            
            for (auto item : rows)
                update_psq(item, true);
            m_readBuffers[getCounterRow(row_addr)].flush();
            return rows.size() > 0;
        }

        void handleType3()
        {
            for(auto const& item : m_psq)
            {
                int row_addr = item.first;
                if (m_counters[row_addr] >= m_alert_thresh) {
                    // PSQ Counter should be the same as in-DRAM counter
                    if (m_counters[row_addr] != m_psq[row_addr]){
                        std::printf("[TOP VICTIM UPDATE][ERROR!] PSQ counter: %lu, and In-DRAM counter: %lu, Have Different Values!\n", m_counters[row_addr], m_psq[row_addr]);
                        assert(m_counters[row_addr] == m_psq[row_addr]);
                    }
                    m_critical_rows[row_addr] = m_counters[row_addr];
                    m_is_abo_needed = true;
                }
            }
            
        }

        int getCounterRow(int row_addr)
        {
            return row_addr / (8 * 1024);
        }

        // Functions for PSQ managements
        bool is_psq_full() {
            if(m_psq.size() > m_psq_size){
                std::printf("Error: PSQ size %ld is larger than the assigned value %ld\n", m_psq.size(), m_psq_size);
                assert(m_psq.size() <= m_psq_size);
            }

            if(m_psq.size() == m_psq_size){
                // if(m_debug)
                //     std::printf("Bank %d, PSQ is Full! Current Size: %d\n", m_bank_id, m_psq.size());
                return true;
            }
            // if(m_debug)
            //     std::printf("Bank %d, PSQ is not Full! Current Size: %d\n",m_bank_id, m_psq.size());
       
            return false;
        }

        bool replace_psq_entry(auto row_addr) {
            auto min_entry = std::min_element(m_psq.begin(), m_psq.end(), 
                    [](const auto& lhs, const auto& rhs) {
                        return lhs.second < rhs.second;
                    });
            s_q_counter_writes++;
            // if (m_debug){
            //     std::printf("Current Minimum Row Id: %d, Cnt: %d\n", min_entry->first, min_entry->second);
            //     std::printf("Accesed Row Id: %d, Cnt: %d\n", row_addr, m_counters[row_addr]);
            // }
            // Replacement is performed --> Return true;
            if (m_counters[row_addr] > min_entry->second) {
                if (m_debug)
                    std::printf("Replace Row %d with Row %d\n", min_entry->first, row_addr);
                m_psq[row_addr] = m_counters[row_addr];
                if (min_entry->second >= m_alert_thresh){
                    // Remove this entry from critical entry since this row cannot be tracked from DRAM
                    m_critical_rows.erase(min_entry->first);
                }
                
                int cache_evict_tag;
                if (m_pb_counter_cache.access(min_entry->first, m_bank_id) == -1 && 
                    (cache_evict_tag = m_pb_counter_cache.insert(min_entry->first, m_counters[min_entry->first] , m_bank_id)) != -1)
                {
                    // We couldn't save a writeback to the DRAM
                    s_cached_counter_writes++;
                    if (m_writeBuffers[getCounterRow(cache_evict_tag)].insert(cache_evict_tag ,m_counters[cache_evict_tag]))
                    {   
                        // We record the writeback flush from ABO as one write here.
                        if (!m_is_abo_needed)
                            s_wb_abo++;
                        m_is_abo_needed = true;
                    }
                    // std::cerr << m_writeBuffers[getCounterRow(min_entry->first)].buffer.size() << '\n';
                }
                m_psq.erase(min_entry->first);
                
                // s_counter_writes++;
                
                return true;
            }
            return false;
            
        }

        // Return values:
        // 0: If it's internally incremented, 1: If it's inserted w/o replacement 
        // -1: If it's not inserted, 2: If it's inserted w/ replacement
        // 3: if burst happen, have to check all element in PSQ.
        int update_psq(auto row_addr, bool isRecurse = false) {
            // 1. Check if entry is already in the PSQ
            int buf_id;
            int ret = -1;
            if (m_psq.find(row_addr) != m_psq.end()) {
                s_queue_hits++;
                m_psq[row_addr]++;
                if (!isRecurse && (buf_id = tryFlushMaxWB()) != -1)
                {
                    s_rwb_counter_writes++;
                    s_wb_counter_writes++;
                    return tryFlushRB(buf_id) ? 3 : 0;
                }
                return 0;
            }
            else{
                s_q_counter_reads++;
                s_queue_misses++;

                // Counter cache hits
                int cache_evict_tag;
                if (m_pb_counter_cache.access(row_addr, m_bank_id) != -1)
                {
                    s_pb_cache_hits++;
                    if (!isRecurse && (buf_id = tryFlushMaxWB()) != -1)
                    {
                        s_rwb_counter_writes++;
                        s_wb_counter_writes++;
                        ret = tryFlushRB(buf_id) ? 3 : -1;
                    }
                }
                else {

                    // Given you found the entry in the writeback
                    if (!m_writeBuffers[getCounterRow(row_addr)].find(row_addr))
                    {
                        // Record a read. 
                        s_wb_counter_reads++;
                        
                        if (!isRecurse)
                        {
                            m_readBuffers[getCounterRow(row_addr)].insert(row_addr);
                            if (m_readBuffers[getCounterRow(row_addr)].isFull())
                            {
                                s_rwb_counter_reads++;
                                m_writeBuffers[getCounterRow(row_addr)].flush();
                                return tryFlushRB(row_addr) ? 3 : -1;
                            }
                            else
                                return -1;
                        }
                    }
                    else if (!isRecurse && (buf_id = tryFlushMaxWB()) != -1)
                    {
                        s_wb_counter_writes++;
                        s_rwb_counter_writes++;
                        ret = tryFlushRB(buf_id) ? 3 : -1;      
                    }

                    if ((cache_evict_tag = m_pb_counter_cache.insert(row_addr, m_counters[row_addr] , m_bank_id)) != -1)
                    {
                        s_cached_counter_writes++;
                        if (m_writeBuffers[getCounterRow(cache_evict_tag)].insert(row_addr,m_counters[cache_evict_tag]))
                        {
                            // We record the writeback flush from ABO as one write here.
                            if (!m_is_abo_needed)
                                s_wb_abo++;
                            m_is_abo_needed = true;
                        }
                    }
                    s_pb_cache_misses++;
                    s_cached_counter_reads++;
                }

                // 2.1 Check if counter reaches enqueueing threshold
                if (m_counters[row_addr] < m_enqueuing_th) {
                    return ret;
                }
                else {
                    //2.2 Insert or replace the entry
                    s_qprac_total_dynamic_energy += qprac_per_bank_access_energy;
                    //2.2.1 Check if queue has an empty entry
                    if(!is_psq_full()) {
                        //2.2.2 Insert the entry into the empty space
                        m_psq[row_addr] = m_counters[row_addr];
                        return ret == -1 ? 1 : ret;
                    }
                    else {
                        //2.2.3 Replace the entry
                        if(replace_psq_entry(row_addr))
                            return ret == -1 ? 2 : ret;
                        else
                            return ret;
                    }
                }
            }
        }
        // Increase the victim rows' counters at each mitigation
        void increase_victim_counters(auto row_addr) {
            // 1. Update upper counter vlaues
            for (int up = 1 ; up <=2; up++){
                auto top_victim = row_addr - up;
                if (top_victim < 0) {
                    continue;
                }
                else {
                    if(m_counters.find(top_victim) == m_counters.end()) {
                        m_counters[top_victim] = 0;
                    }
                    m_counters[top_victim]++;

                    // Read and Write
                    s_counter_reads++; s_counter_writes++;
                    
                    // If current row is not inserted into psq then do nothing
                    int update_type = update_psq(top_victim);
                    if (update_type == -1){
                        return;
                    }
                    else if(update_type >= 0 && update_type <=2){
                        // Asserts Alert if counter reaches NBO and the row is in PSQ
                        if (m_counters[top_victim] >= m_alert_thresh) {
                            // PSQ Counter should be the same as in-DRAM counter
                            if (m_counters[top_victim] != m_psq[top_victim]){
                                std::printf("[TOP VICTIM UPDATE][ERROR!] PSQ counter: %lu, and In-DRAM counter: %lu, Have Different Values!\n", m_counters[top_victim], m_psq[top_victim]);
                                assert(m_counters[top_victim] == m_psq[top_victim]);
                            }
                            m_critical_rows[top_victim] = m_counters[top_victim];
                            m_is_abo_needed = true;
                        }
                    }
                    else if (update_type == 3)
                    {
                        handleType3();
                    }
                }
            }
            //2. Update bottom counter values
            for (int down = 1 ; down <=2; down++) {
                auto bottom_victim = row_addr - down;
                if (bottom_victim >= m_cfg.m_num_rows_per_bank) {
                    continue;
                }
                else {
                    if(m_counters.find(bottom_victim) == m_counters.end()){
                        m_counters[bottom_victim] = 0;
                    }
                    m_counters[bottom_victim]++;
                    s_counter_reads++; s_counter_writes++;
                    // Read and potentially a write back
                    int update_type = update_psq(bottom_victim);

                    // If current row is not inserted into psq then do nothing
                    if (update_type == -1){
                        return;
                    }
                    else if(update_type >= 0 && update_type <=2){
                        // Asserts Alert if counter reaches NBO and the row is in PSQ
                        if (m_counters[bottom_victim] >= m_alert_thresh) {
                            // PSQ Counter should be the same as in-DRAM counter
                            if (m_counters[bottom_victim] != m_psq[bottom_victim]){
                                std::printf("[BOTTOM VICTIM UPDATE][ERROR!] PSQ counter: %lu, and In-DRAM counter: %lu, Have Different Values!\n", m_counters[bottom_victim], m_psq[bottom_victim]);
                                assert(m_counters[bottom_victim] == m_psq[bottom_victim]);
                            }
                            m_critical_rows[bottom_victim] = m_counters[bottom_victim];
                            m_is_abo_needed = true;
                        }
                    }
                    else if (update_type == 3)
                    {
                        handleType3();
                    }
                }
            }
        }
        // PSQ Mitigations -- Mitigation Type 0: RFM, 1: Targeted REF
        void process_psq_mitigation(int mitigation_type) {
            auto row_addr = -1;
            auto max_entry = std::max_element(m_psq.begin(), m_psq.end(),
                [] (const std::pair<int, uint32_t>& p1, const std::pair<int, uint32_t>& p2) {
                    return p1.second < p2.second;
                });
            // 1.Check if PSQ is empty
            if (max_entry == m_psq.end()){
                return;
            }

            // 1.1 Only for the RFMs, check if opportunistic mitigation is enabled
            if (mitigation_type == 0 && !m_enable_opportunistic_mitigation && m_counters[max_entry->first] < m_alert_thresh){
                if (m_debug){
                    std::printf("No Opportunitic Mitigation: Skips Ba: %d Cnt: %lu\n", m_bank_id, m_counters[max_entry->first]);
                }
                return;
            }
            // 1.2. Only for the targeted refreshes (proactive mitigations)
            if (mitigation_type == 1 && m_counters[max_entry->first] < m_proactive_mitigation_th){
                if (m_debug){
                    std::printf("[TARGETED REF]: MAX CTR is smaller than mitigation threshold! --> Skips Ba: %d Cnt: %lu\n", m_bank_id, m_counters[max_entry->first]);
                }
                return;               
            }
            // 2. Perform mitigations
            // 2.1 Reset counter value and remove the entry from psq
            m_counters[max_entry->first] = 0;
            row_addr = max_entry->first;
            m_critical_rows.erase(max_entry->first);
            
            int cache_evict_tag;
            if (m_pb_counter_cache.access(max_entry->first, m_bank_id) == -1 && 
                (cache_evict_tag = m_pb_counter_cache.insert(max_entry->first, m_counters[max_entry->first] , m_bank_id)) != -1)
                {
                    // We couldn't save a writeback to the DRAM
                    s_cached_counter_writes++;
                    if (m_writeBuffers[getCounterRow(cache_evict_tag)].insert(cache_evict_tag, m_counters[cache_evict_tag]))
                    {
                        // We record the writeback flush from ABO as one write here.
                        if (!m_is_abo_needed)
                            s_wb_abo++;
                        m_is_abo_needed = true;
                    }
                }
            m_psq.erase(max_entry->first);
            s_q_counter_writes++;

            s_num_total_mitigations++;
            s_qprac_total_dynamic_energy += qprac_per_bank_access_energy;
            // 2.2 Perform mitigations on victims --> Increase victim counters
            increase_victim_counters(row_addr);
        }

        void process_targeted_ref (const Request& req) {
            // 1. Check if Targeted REF is enabled  
            if (m_targeted_ref_frequency == 0)
                return;
            
            m_num_ref++;
            // 2. Check if this refresh is for Targeted REF
            if (m_num_ref % m_targeted_ref_frequency != 0)
                return;
            // 3. Perform mitigation for top-most activated row
            process_psq_mitigation(1);
            if(m_bank_id == 0)
                s_num_targeted_ref += m_cfg.m_num_ranks;
        }

        void process_act(const Request& req) {
            auto row_addr = req.addr_vec[m_cfg.m_row_level];    
            if (m_counters.find(row_addr) == m_counters.end()) {
                if (!m_random_counter_initializeion){
                    m_counters[row_addr] = 0; 
                    m_counters[row_addr]++;
                }
                // When simulation starts with randomly inialized counters.
                else{
                    gen = std::mt19937(req.addr_vec[1]*2926+m_bank_id*42+row_addr);  
                    dist = std::uniform_int_distribution<int>(0, m_alert_thresh-1);  
                    m_counters[row_addr] = dist(gen);  // Assign a random value between 0 and m_alert_thresh
                    if(m_counters[row_addr] == 0)
                        m_counters[row_addr]++;
                    // Debug
                    if (m_debug)
                        std::printf("[Debug] Initialize counter for Rank: %d, BG: %d, Bank: %d, Row: %d, CNT Value: %d\n", req.addr_vec[1], req.addr_vec[2], req.addr_vec[3], row_addr, m_counters[row_addr]);
                }
            }
            else{
                m_counters[row_addr]++;
            }
            // if (m_debug) {
            //     std::printf("[PRAC] [%d] [ACT] Row: %d Act: %u\n",
            //         m_bank_id, row_addr, m_counters[row_addr]);
            // }
            // If current row is not inserted into psq then do nothing

            // Read and potentially a write back
            s_counter_reads++; s_counter_writes++;
            // m_writeBuffers[getCounterRow(row_addr)].flush();
            int update_type = update_psq(row_addr);

            if (update_type == -1){
                return;
            }
            else if(update_type >= 0 && update_type <= 2){
                // Asserts Alert if counter reaches NBO and the row is in PSQ
                if (m_counters[row_addr] >= m_alert_thresh) {
                    // PSQ Counter should be the same as in-DRAM counter
                    if (m_counters[row_addr] != m_psq[row_addr]){
                        std::printf("[ERROR!] PSQ counter: %lu, and In-DRAM counter: %lu, Have Different Values!\n", m_counters[row_addr], m_psq[row_addr]);
                        assert(m_counters[row_addr] == m_psq[row_addr]);
                    }
                    if (m_debug){
                        std::printf("[ASSERT ALERT] Bank id %d, Row id %d, counter vlaue %d\n", m_bank_id, row_addr, m_counters[row_addr]);
                    }
                    m_critical_rows[row_addr] = m_counters[row_addr];
                    m_is_abo_needed = true;
                }
            }
            else if (update_type == 3)
                    {
                        handleType3();
                    }
            else {
                std::printf("[ERROR!] PSQ Update Returns Wrong Value!\n");
                assert(update_type <= 3);
            }
        }

        void process_rfm(const Request& req) {
            tryFlushMaxWB();
                    
            process_psq_mitigation(0);
        }
    };  // class PerBankCounters

};      // class QPRAC

}       // namespace Ramulator
