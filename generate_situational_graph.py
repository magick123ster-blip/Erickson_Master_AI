import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import re

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.csv')

def get_macro(pid):
    if 'PACING' in pid: return 'PACING'
    if 'SUGGESTION' in pid: return 'SUGGESTION'
    if 'CONFUSION' in pid: return 'CONFUSION'
    if 'INDUCTION' in pid: return 'INDUCTION'
    if 'METAPHOR' in pid: return 'METAPHOR'
    if 'UTILIZATION' in pid: return 'UTILIZATION'
    if 'DISSOCIATION' in pid: return 'DISSOCIATION'
    if 'RATIFICATION' in pid: return 'RATIFICATION'
    if 'FUTURE_PACING' in pid: return 'FUTURE_PACING'
    return 'OTHER'

color_map_base = {
    'PACING': '#5C6BC0',      # Indigo
    'SUGGESTION': '#FF7043',   # Coral
    'CONFUSION': '#AB47BC',    # Purple (Violet)
    'INDUCTION': '#26A69A',    # Teal
    'METAPHOR': '#FFCA28',     # Gold (Amber)
    'UTILIZATION': '#66BB6A',  # Green
    'DISSOCIATION': '#23D5AB', # Cyan-ish
    'RATIFICATION': '#26C6DA', # Blue Cyan
    'FUTURE_PACING': '#FFA726',# Orange
    'OTHER': '#BDBDBD'         # Gray
}

def draw_network(df_subset, output_path, title, is_master=False):
    G = nx.DiGraph()
    node_freq = {}
    edges = {}
    
    cols = [c for c in df_subset.columns if c.startswith('step_') and c.endswith('_id')]
    
    for _, row in df_subset.iterrows():
        chain = [row[c] for c in cols if not pd.isna(row[c])]
        for i in range(len(chain)):
            node = chain[i]
            node_freq[node] = node_freq.get(node, 0) + 1
            if i < len(chain) - 1:
                next_node = chain[i+1]
                edge = (node, next_node)
                edges[edge] = edges.get(edge, 0) + 1
                
    for node, freq in node_freq.items():
        G.add_node(node, size=freq, macro=get_macro(node))
    for (u, v), weight in edges.items():
        G.add_edge(u, v, weight=weight)
        
    figsize = (24, 18) if is_master else (16, 12)
    plt.figure(figsize=figsize, dpi=120)
    plt.style.use('dark_background')
    
    pos = nx.spring_layout(G, k=1.0 if is_master else 1.5, iterations=50, seed=42)
    
    node_colors = [color_map_base.get(G.nodes[node]['macro'], '#BDBDBD') for node in G.nodes()]
    node_sizes = [G.nodes[node]['size'] * (150 if is_master else 300) + (400 if is_master else 600) for node in G.nodes()]
    
    edge_weights = [G.edges[u, v]['weight'] for u, v in G.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    nx.draw_networkx_edges(G, pos, width=[(w/max_w)*4 + 0.5 for w in edge_weights], 
                           edge_color='white', alpha=0.3, arrows=True, arrowsize=20)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=7 if is_master else 9, font_family='sans-serif', font_color='white', font_weight='bold')
    
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=k,
                              markerfacecolor=v, markersize=10) for k, v in color_map_base.items() if any(G.nodes[n]['macro'] == k for n in G.nodes())]
    plt.legend(handles=legend_elements, loc='upper right', title="Macro Category", fontsize=10, title_fontsize=12)

    plt.title(title, fontsize=24 if is_master else 18, pad=20, color='white')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, facecolor='black', bbox_inches='tight')
    plt.close()
    print(f"Graph saved: {output_path}")

def draw_elite_network(df_subset, output_path, title):
    G = nx.DiGraph()
    node_freq = {}
    edges = {}
    
    cols = [c for c in df_subset.columns if c.startswith('step_') and c.endswith('_id')]
    
    all_pids = []
    for _, row in df_subset.iterrows():
        all_pids.extend([row[c] for c in cols if not pd.isna(row[c])])
    elite_7 = pd.Series(all_pids).value_counts().head(7).index.tolist()
    
    for _, row in df_subset.iterrows():
        chain = [row[c] for c in cols if not pd.isna(row[c])]
        for i in range(len(chain)):
            node = chain[i]
            if node in elite_7:
                node_freq[node] = node_freq.get(node, 0) + 1
                if i < len(chain) - 1:
                    next_node = chain[i+1]
                    if next_node in elite_7:
                        edge = (node, next_node)
                        edges[edge] = edges.get(edge, 0) + 1
                
    for node in elite_7:
        freq = node_freq.get(node, 0)
        G.add_node(node, size=freq, macro=get_macro(node))
    for (u, v), weight in edges.items():
        out_weight = sum([w for (src, dst), w in edges.items() if src == u])
        prob = weight / out_weight if out_weight > 0 else 0
        G.add_edge(u, v, weight=weight, prob=prob)
        
    plt.figure(figsize=(14, 10), dpi=120)
    plt.style.use('dark_background')
    
    pos = nx.circular_layout(G)
    node_colors = [color_map_base.get(G.nodes[node]['macro'], '#BDBDBD') for node in G.nodes()]
    node_sizes = [G.nodes[node]['size'] * 400 + 1000 for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9, edgecolors='white', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', font_color='white', font_weight='bold')
    
    ax = plt.gca()
    for u, v, data in G.edges(data=True):
        prob_pct = data['prob'] * 100
        edge_label = f"{prob_pct:.1f}%"
        nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], width=data['weight']*1.5, 
                               edge_color='white', alpha=0.4, arrows=True, arrowsize=20,
                               connectionstyle="arc3,rad=0.2")
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        ax.text(x, y + 0.05, edge_label, fontsize=8, color='yellow', fontweight='bold', ha='center',
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', pad=1))

    plt.title(title, fontsize=20, pad=20, color='white')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, facecolor='black', bbox_inches='tight')
    plt.close()
    print(f"Elite Graph saved: {output_path}")

def generate_all_graphs():
    df = pd.read_csv(INPUT_CSV)
    
    # 1. Master Graph
    master_path = os.path.join(DATA_DIR, 'erickson_master_strategic_network.png')
    draw_network(df, master_path, 'Milton Erickson Master Strategic Network (All 70 Chains)', is_master=True)
    
    # 2. Situational Graphs
    for situation, group in df.groupby('situation'):
        slug = re.sub(r'[^a-z0-9]', '_', situation.lower()).strip('_')
        slug = re.sub(r'_+', '_', slug)
        
        # A. Full Situational Network
        sit_path = os.path.join(DATA_DIR, f'erickson_graph_{slug}.png')
        draw_network(group, sit_path, f'Full Strategic Network: {situation}')
        
        # B. Elite 7 Relationship Map
        elite_path = os.path.join(DATA_DIR, f'erickson_elite_7_graph_{slug}.png')
        draw_elite_network(group, elite_path, f'Elite 7 Relationship Map: {situation}')

if __name__ == "__main__":
    generate_all_graphs()
