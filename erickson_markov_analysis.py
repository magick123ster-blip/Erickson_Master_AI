import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def run_markov_analysis():
    # 1. Load Data
    print("Loading sequence data...")
    df = pd.read_csv(INPUT_CSV)
    
    # Ensure sorting (though it should be sorted already from the prep script)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    # 2. Generate Transition Pairs
    print("Generating transition pairs...")
    transitions = []
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_label'].tolist()
        for i in range(len(patterns) - 1):
            transitions.append((patterns[i], patterns[i+1]))
    
    # 3. Build Transition Probability Matrix
    print("Building transition matrix...")
    matrix = pd.crosstab(
        pd.Series([t[0] for t in transitions], name='Current'),
        pd.Series([t[1] for t in transitions], name='Next'),
        normalize='index'
    )
    
    print("\nTransition Probability Matrix:")
    print(matrix)
    
    # 4. Visualization: Heatmap
    print("\nGenerating Heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Milton Erickson Pattern Transition Heatmap')
    plt.tight_layout()
    heatmap_path = os.path.join(DATA_DIR, 'erickson_heatmap.png')
    plt.savefig(heatmap_path)
    print(f"Heatmap saved to {heatmap_path}")
    
    # 5. Visualization: State Transition Diagram (NetworkX)
    print("Generating Transition Diagram...")
    plt.figure(figsize=(12, 10))
    G = nx.DiGraph()
    
    # Build edges from matrix where prob > 0.05 (slightly lower than 0.1 for more detail)
    threshold = 0.05
    for i in matrix.index:
        for j in matrix.columns:
            prob = matrix.loc[i, j]
            if prob > threshold:
                G.add_edge(i, j, weight=prob)
    
    pos = nx.spring_layout(G, seed=42, k=2.0)
    nx.draw(G, pos, with_labels=True, node_size=3500, node_color='skyblue', 
            font_size=10, font_weight='bold', arrows=True, arrowsize=20, edge_color='gray', alpha=0.8)
    
    labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f'{v:.2f}' for k, v in labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    plt.title('Milton Erickson Pattern State Transition Diagram')
    plt.tight_layout()
    graph_path = os.path.join(DATA_DIR, 'erickson_transition_graph.png')
    plt.savefig(graph_path)
    print(f"Transition Diagram saved to {graph_path}")
    
    # 6. Advanced Analysis: Stationary Distribution (Steady State)
    print("\nCalculating Stationary Distribution...")
    # Using the matrix as a transition matrix P
    P = matrix.values
    # Solving for pi * P = pi  => P.T * pi.T = pi.T
    evals, evecs = np.linalg.eig(P.T)
    
    # Find the eigenvector corresponding to eigenvalue 1
    # We take the real part as the probabilities should be real
    idx = np.argmin(np.abs(evals - 1.0))
    stationary = evecs[:, idx].real
    
    # Normalize so it sums to 1
    stationary = stationary / stationary.sum()
    
    pattern_importance = pd.Series(stationary, index=matrix.index)
    sorted_importance = pattern_importance.sort_values(ascending=False)
    
    print("\nStationary Distribution (Long-term probability of states):")
    print(sorted_importance)
    
    # Save the stationary distribution to a CSV for later use
    sorted_importance.to_csv(os.path.join(DATA_DIR, 'stationary_distribution.csv'))
    
    return matrix, sorted_importance

if __name__ == "__main__":
    run_markov_analysis()
