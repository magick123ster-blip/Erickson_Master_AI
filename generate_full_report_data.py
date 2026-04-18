import pandas as pd
import numpy as np
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def generate_full_report():
    print("Loading sequence data for zero-loss analysis...")
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    # 1. Extract ALL transitions
    print("Mapping 100% of transitions...")
    transitions = []
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 1):
            transitions.append((patterns[i], patterns[i+1]))
    
    all_trans_df = pd.DataFrame(transitions, columns=['Current', 'Next'])
    
    # Calculate probabilities
    counts = all_trans_df.groupby(['Current', 'Next']).size().reset_index(name='Count')
    total_out = all_trans_df.groupby('Current').size().reset_index(name='Total_Out')
    counts = counts.merge(total_out, on='Current')
    counts['Probability'] = counts['Count'] / counts['Total_Out']
    
    # Export full transition database
    counts.to_csv(os.path.join(DATA_DIR, 'complete_strategic_map.csv'), index=False)
    print(f"Exported {len(counts)} unique transitions.")
    
    # 2. Calculate Full Stationary Distribution
    print("Calculating stationary distribution for all nodes...")
    unique_patterns = sorted(list(set(all_trans_df['Current'].unique()) | set(all_trans_df['Next'].unique())))
    p_map = {p: i for i, p in enumerate(unique_patterns)}
    N = len(unique_patterns)
    
    P = np.zeros((N, N))
    for _, row in counts.iterrows():
        P[p_map[row['Current']], p_map[row['Next']]] = row['Probability']
    
    # Power iteration
    pi = np.ones(N) / N
    for _ in range(100):
        pi = pi @ P
    
    importance_df = pd.DataFrame({
        'pattern_id': unique_patterns,
        'importance_score': pi
    }).sort_values(by='importance_score', ascending=False)
    
    importance_df.to_csv(os.path.join(DATA_DIR, 'full_stationary_distribution.csv'), index=False)
    print(f"Calculated importance for {N} patterns.")

    # 3. Hierarchical Grouping for Markdown Report
    print("Organizing hierarchical data...")
    # Add parents/children info for the report
    report_data = []
    for p_id in unique_patterns:
        # Children (What this pattern leads to)
        children = counts[counts['Current'] == p_id].sort_values(by='Probability', ascending=False).head(3)
        children_str = "; ".join([f"{row['Next']} ({row['Probability']:.2f})" for _, row in children.iterrows()])
        
        # Parents (What leads to this pattern)
        parents = counts[counts['Next'] == p_id].sort_values(by='Probability', ascending=False).head(2)
        parents_str = "; ".join([f"{row['Current']} ({row['Probability']:.2f})" for _, row in parents.iterrows()])
        
        # Categorization by prefix
        prefix = "OTHER"
        if "_" in p_id:
            parts = p_id.split("_")
            if len(parts) > 1:
                prefix = parts[1] # e.g., ERICKSON_UTILIZATION -> UTILIZATION
        
        score = importance_df[importance_df['pattern_id'] == p_id]['importance_score'].values[0]
        
        report_data.append({
            'Category': prefix,
            'Pattern ID': p_id,
            'Importance': score,
            'Typical Leads To': children_str,
            'Typical Preceded By': parents_str
        })
    
    final_report_df = pd.DataFrame(report_data)
    final_report_df.to_csv(os.path.join(DATA_DIR, 'hierarchical_report_source.csv'), index=False)
    print("Hierarchical source data generated.")

if __name__ == "__main__":
    generate_full_report()
