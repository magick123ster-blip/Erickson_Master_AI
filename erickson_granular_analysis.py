import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def run_granular_analysis():
    print("Loading data for granular analysis...")
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    # Generate transitions at pattern_id level
    print("Extracting pattern-to-pattern transitions...")
    transitions = []
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 1):
            transitions.append((patterns[i], patterns[i+1]))
    
    trans_df = pd.DataFrame(transitions, columns=['Current', 'Next'])
    
    # Calculate counts and probabilities
    counts = trans_df.groupby(['Current', 'Next']).size().reset_index(name='Count')
    total_out = trans_df.groupby('Current').size().reset_index(name='Total')
    counts = counts.merge(total_out, on='Current')
    counts['Probability'] = counts['Count'] / counts['Total']
    
    # 1. FIND TOP CONNECTIONS
    print("\n[Finding Strongest Connections]")
    top_connections = counts.sort_values(by=['Count', 'Probability'], ascending=False).head(50)
    print(top_connections[['Current', 'Next', 'Count', 'Probability']])
    
    # 2. FIND INTERVENTION CHAINS (A -> B -> C)
    print("\n[Identifying Intervention Chains]")
    # We look for transitions that lead to "Suggestion" type patterns
    suggestion_patterns = top_connections[top_connections['Next'].str.contains('SUGGESTION|ACTION|DIRECTIVE|COMMAND', case=False, na=False)]
    print("Transitions leading to Sugggestions/Actions:")
    print(suggestion_patterns[['Current', 'Next', 'Count', 'Probability']])

    # 3. STATIONARY DISTRIBUTION (STAYING POWER)
    print("\n[Calculating Stationary Distribution for 3,000+ Patterns]")
    # Due to the size, we'll use a sparse-friendly approach or top patterns
    unique_patterns = list(set(trans_df['Current'].unique()) | set(trans_df['Next'].unique()))
    p_map = {p: i for i, p in enumerate(unique_patterns)}
    N = len(unique_patterns)
    
    # Create the transition matrix P
    # We can use a simpler power iteration or just rank by frequency if memory is tight,
    # but let's try a dense calculation first if N is manageable (N is unique patterns in scripts, not the full 3,976)
    print(f"Unique patterns found in scripts: {N}")
    
    if N < 5000: # Safety check
        P = np.zeros((N, N))
        for _, row in counts.iterrows():
            P[p_map[row['Current']], p_map[row['Next']]] = row['Probability']
        
        # Power iteration to find stationary distribution (pi * P = pi)
        # pi_0 * P^100 or similar
        pi = np.ones(N) / N
        for _ in range(50):
            pi = pi @ P
        
        importance = pd.Series(pi, index=unique_patterns).sort_values(ascending=False)
        print("\nTop 20 Critical Micro-Patterns (Stationary Distribution):")
        print(importance.head(20))
        importance.to_csv(os.path.join(DATA_DIR, 'granular_stationary_distribution.csv'))
    
    # 4. VISUALIZATION (SUB-GRAPH of TOP 30 TRANSITIONS)
    print("\n[Generating Granular Connection Graph]")
    plt.figure(figsize=(16, 12))
    G = nx.DiGraph()
    
    # Use top 40 connections for the graph to keep it readable
    graph_data = counts.sort_values(by='Count', ascending=False).head(40)
    
    for _, row in graph_data.iterrows():
        G.add_edge(row['Current'], row['Next'], weight=row['Probability'], count=row['Count'])
    
    pos = nx.spring_layout(G, k=1.5, seed=42)
    # Node sizing based on relative frequency in this sub-graph
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightcoral', 
            font_size=7, font_weight='bold', arrows=True, arrowsize=15, edge_color='gray', alpha=0.7)
    
    # Edge labels (count/prob)
    edge_labels = { (u, v): f"{d['weight']:.2f}\n({d['count']})" for u, v, d in G.edges(data=True) }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    
    plt.title('Top Granular Pattern Connections in Erickson Therapy')
    plt.tight_layout()
    graph_path = os.path.join(DATA_DIR, 'erickson_granular_graph.png')
    plt.savefig(graph_path)
    print(f"Granular Graph saved to {graph_path}")

    # Output top connections to CSV for the report
    top_connections.to_csv(os.path.join(DATA_DIR, 'top_granular_connections.csv'), index=False)
    
if __name__ == "__main__":
    run_granular_analysis()
