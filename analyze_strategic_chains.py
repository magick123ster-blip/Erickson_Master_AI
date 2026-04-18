import pandas as pd
import re
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
HIERARCHY_FILE = os.path.join(DATA_DIR, 'hierarchical_report_source.csv')
MASTER_FILE = os.path.join(DATA_DIR, 'erickson_master_analysis_data.csv')
OUTPUT_CSV = os.path.join(DATA_DIR, 'erickson_all_strategic_chains.csv')

def parse_leads_to(leads_to_str):
    if pd.isna(leads_to_str) or leads_to_str == "":
        return []
    parts = leads_to_str.split(';')
    results = []
    for p in parts:
        match = re.search(r'(\w+)\s*\((\d+\.?\d*)\)', p)
        if match:
            results.append((match.group(1), float(match.group(2))))
    return results

def extract_all_chains():
    print("Loading data...")
    df_h = pd.read_csv(HIERARCHY_FILE)
    df_m = pd.read_csv(MASTER_FILE)
    
    df_m_unique = df_m.drop_duplicates(subset='pattern_id')
    master_lookup = df_m_unique.set_index('pattern_id')[['output', 'svo_structure', 'reasoning']].to_dict('index')
    
    adj = {}
    total_transitions = 0
    for _, row in df_h.iterrows():
        pid = row['Pattern ID']
        leads = parse_leads_to(row['Typical Leads To'])
        # Threshold 0.3
        valid_leads = [l for l in leads if l[1] >= 0.3]
        adj[pid] = valid_leads
        total_transitions += len(valid_leads)
    
    print(f"Built adjacency list with {len(adj)} nodes and {total_transitions} valid transitions.")
    
    chains = []
    all_starts = [pid for pid, leads in adj.items() if leads]
    print(f"\nStarting chain exploration from all {len(all_starts)} patterns...")

    for start_node in all_starts:
        current_chain = [start_node]
        seen = {start_node}
        curr = start_node
        
        for _ in range(9): # Max 10 steps
            next_nodes = adj.get(curr, [])
            if not next_nodes:
                break
            next_node, prob = max(next_nodes, key=lambda x: x[1])
            if next_node in seen:
                break
            current_chain.append(next_node)
            seen.add(next_node)
            curr = next_node
            
        if len(current_chain) >= 3:
            chains.append(current_chain)
    
    # Sort by length and deduplicate
    unique_chains = []
    seen_chains = set()
    for c in sorted(chains, key=len, reverse=True):
        chain_tuple = tuple(c)
        if chain_tuple not in seen_chains:
            unique_chains.append(c)
            seen_chains.add(chain_tuple)

    print(f"Total unique chains found: {len(unique_chains)}")

    # Exporting all chains to CSV
    export_rows = []
    for i, chain in enumerate(unique_chains):
        chain_str = " -> ".join(chain)
        # Detailed row for each pattern in the chain? Or one row per chain?
        # Let's do a structured format where each chain is a row.
        row = {
            "chain_no": i + 1,
            "length": len(chain),
            "chain_sequence": chain_str
        }
        # Add pattern details for the first 10 steps
        for j, pid in enumerate(chain):
            info = master_lookup.get(pid, {"output": "[N/A]"})
            row[f"step_{j+1}_id"] = pid
            row[f"step_{j+1}_text"] = str(info['output'])[:200]
            
        export_rows.append(row)

    df_export = pd.DataFrame(export_rows)
    df_export.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"Successfully exported {len(unique_chains)} chains to {OUTPUT_CSV}")

if __name__ == "__main__":
    extract_all_chains()
