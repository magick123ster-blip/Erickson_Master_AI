import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import os
import random

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

# Simulated Reaction Weights for Erickson's 8 Macro Patterns
# Columns: ['COMPLIANCE', 'RESISTANCE', 'CONFUSION', 'TRANCE_DEEPENING', 'AWARENESS_SHIFT']
CLIENT_STATES = ['COMPLIANCE', 'RESISTANCE', 'CONFUSION', 'TRANCE_DEEPENING', 'AWARENESS_SHIFT']

REACTION_WEIGHTS = {
    'PACING': [0.70, 0.05, 0.05, 0.10, 0.10],
    'UTILIZATION': [0.40, 0.10, 0.10, 0.20, 0.20],
    'DOUBLE_BIND': [0.20, 0.10, 0.40, 0.10, 0.20],
    'CONFUSION': [0.10, 0.20, 0.60, 0.00, 0.10],
    'TRUISM': [0.60, 0.05, 0.05, 0.15, 0.15],
    'REFRAMING': [0.20, 0.15, 0.15, 0.10, 0.40],
    'SUGGESTION': [0.40, 0.20, 0.05, 0.30, 0.05],
    'OTHER': [0.40, 0.20, 0.10, 0.10, 0.20]
}

def simulate_client_response(therapist_pattern):
    weights = REACTION_WEIGHTS.get(therapist_pattern, REACTION_WEIGHTS['OTHER'])
    return np.random.choice(CLIENT_STATES, p=weights)

def run_bipartite_analysis():
    print("Loading sequence data for Bipartite Analysis...")
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    print("Simulating Client Responses and Building Bipartite Sequences...")
    # Bipartite tracking
    t_to_c_transitions = [] # Therapist -> Client
    c_to_t_transitions = [] # Client -> Therapist
    
    np.random.seed(42) # For reproducible simulation
    
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_label'].str.upper().tolist()
        
        # For each therapist pattern, a client responds, then the therapist speaks again
        for i in range(len(patterns) - 1):
            t_current = patterns[i]
            # Handle Double Bind space issue if any
            if t_current == 'DOUBLE BIND':
                t_current = 'DOUBLE_BIND'
            t_next = patterns[i+1]
            if t_next == 'DOUBLE BIND':
                t_next = 'DOUBLE_BIND'
            
            # Predict simulation of what client did after t_current
            c_response = simulate_client_response(t_current)
            
            t_to_c_transitions.append((t_current, c_response))
            # Client responds, then Erickson transitions to his t_next
            c_to_t_transitions.append((c_response, t_next))

    # 1. Therapist ➡ Client Transition Matrix
    print("Building Therapist -> Client Matrix...")
    tc_matrix = pd.crosstab(
        pd.Series([t[0] for t in t_to_c_transitions], name='Therapist_Action'),
        pd.Series([t[1] for t in t_to_c_transitions], name='Client_Reaction'),
        normalize='index'
    )
    tc_matrix.to_csv(os.path.join(DATA_DIR, 'therapist_to_client_matrix.csv'))
    
    # 2. Client ➡ Therapist Transition Matrix
    print("Building Client -> Therapist Matrix...")
    ct_matrix = pd.crosstab(
        pd.Series([t[0] for t in c_to_t_transitions], name='Client_Reaction'),
        pd.Series([t[1] for t in c_to_t_transitions], name='Therapist_Followup'),
        normalize='index'
    )
    ct_matrix.to_csv(os.path.join(DATA_DIR, 'client_to_therapist_matrix.csv'))

    print("\nClient to Therapist Reaction Base Probabilities:")
    print(ct_matrix)

    # 3. Visualization: Building Bipartite Graph
    print("\nGenerating Bipartite State Transition Graph...")
    B = nx.DiGraph()
    
    therapist_nodes = list(REACTION_WEIGHTS.keys())
    client_nodes = CLIENT_STATES
    
    # Add nodes with bipartite attribute
    B.add_nodes_from(therapist_nodes, bipartite=0)
    B.add_nodes_from(client_nodes, bipartite=1)
    
    # Add edges: T -> C
    for t_node in tc_matrix.index:
        for c_node in tc_matrix.columns:
            prob = tc_matrix.loc[t_node, c_node]
            if prob > 0.15: # threshold
                B.add_edge(t_node, c_node, weight=prob, color='blue')
                
    # Add edges: C -> T
    for c_node in ct_matrix.index:
        for t_node in ct_matrix.columns:
            prob = ct_matrix.loc[c_node, t_node]
            if prob > 0.15: # threshold
                B.add_edge(c_node, t_node, weight=prob, color='orange')
                
    plt.figure(figsize=(14, 10))
    # Separate layouts for bipartite
    pos = {}
    pos.update((node, (1, index)) for index, node in enumerate(therapist_nodes))
    pos.update((node, (2, index + 1.5)) for index, node in enumerate(client_nodes))
    
    edges = B.edges()
    colors = [B[u][v]['color'] for u,v in edges]
    weights = [B[u][v]['weight'] * 5 for u,v in edges]
    
    nx.draw_networkx_nodes(B, pos, nodelist=therapist_nodes, node_color='lightblue', node_size=3000, alpha=0.9)
    nx.draw_networkx_nodes(B, pos, nodelist=client_nodes, node_color='lightgreen', node_size=3000, alpha=0.9)
    
    nx.draw_networkx_edges(B, pos, edgelist=edges, edge_color=colors, width=weights, arrows=True, arrowsize=20, alpha=0.7)
    nx.draw_networkx_labels(B, pos, font_size=10, font_weight='bold')
    
    edge_labels = {(u,v): f"{B[u][v]['weight']:.2f}" for u,v in edges}
    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title('Bipartite Markov Chain: Therapist Interventions ↔ Client Responses', fontsize=15)
    plt.text(1, -1, 'Therapist Interventions', fontsize=12, ha='center', fontweight='bold')
    plt.text(2, -1, 'Client Responses', fontsize=12, ha='center', fontweight='bold')
    plt.axis('off')
    
    graph_path = os.path.join(DATA_DIR, 'erickson_bipartite_graph.png')
    plt.tight_layout()
    plt.savefig(graph_path, dpi=300)
    print(f"Bipartite Diagram saved to {graph_path}")
    
if __name__ == '__main__':
    run_bipartite_analysis()
