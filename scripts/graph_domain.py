import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path
import textwrap

# Define input/output paths
INPUT_PATH = Path("../results/datamesh/domains.csv")
OUTPUT_DIR = Path("../results/datamesh")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def wrap_label(label, width=15):
    """Wrap text labels with improved width for better readability"""
    return textwrap.fill(label, width=width, break_long_words=False)

def create_domain_entity_graph(csv_path):
    """Create graph from CSV data with improved entity handling"""
    df = pd.read_csv(csv_path)
    domain_entities = defaultdict(set)
    
    # Build domain-entity relationships
    for _, row in df.iterrows():
        domain = row['Domain']
        domain_entities[domain].add(row['Entity A'])
        domain_entities[domain].add(row['Entity B'])
    
    # Create and populate graph
    G = nx.Graph()
    domains = list(domain_entities.keys())
    G.add_nodes_from(domains)
    
    # Add edges with shared entities
    for i in range(len(domains)):
        for j in range(i + 1, len(domains)):
            domain1, domain2 = domains[i], domains[j]
            shared_entities = domain_entities[domain1].intersection(domain_entities[domain2])
            if shared_entities:
                # Sort entities for consistent display
                G.add_edge(domain1, domain2, shared_entities=sorted(list(shared_entities)))
    
    return G

def visualize_graph(G, output_path):
    """Create a professional visualization of the domain graph"""
    plt.figure(figsize=(20, 15))
    
    # Use kamada_kawai_layout for better node positioning
    pos = nx.kamada_kawai_layout(G)
    
    # Draw nodes with improved styling
    nx.draw_networkx_nodes(G, pos,
                          node_color='lightblue',
                          node_size=8000,
                          alpha=1.0,
                          edgecolors='gray',
                          linewidths=2)
    
    # Draw edges with better visibility
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          width=2,
                          alpha=0.6)
    
    # Improve node labels
    labels = {node: wrap_label(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels,
                           font_size=11,
                           font_weight='bold',
                           font_family='sans-serif')
    
    # Improve edge labels
    edge_labels = nx.get_edge_attributes(G, 'shared_entities')
    edge_labels = {k: '\n'.join(v) for k, v in edge_labels.items()}
    
    # Add background to edge labels for better readability
    bbox_props = dict(boxstyle="round,pad=0.3",
                     fc="white",
                     ec="gray",
                     alpha=0.8)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels,
                                font_size=9,
                                bbox=bbox_props,
                                rotate=False)
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save with high quality
    plt.savefig(output_path,
                dpi=300,
                bbox_inches='tight',
                pad_inches=0.5,
                facecolor='white')
    plt.close()

def export_graph_data(G, output_path):
    """Export graph data with improved formatting"""
    with open(output_path, 'w') as f:
        f.write("Domain Relationships Analysis\n")
        f.write("=" * 30 + "\n\n")
        
        # Write domains section
        f.write("Domains:\n")
        for node in sorted(G.nodes()):
            f.write(f"- {node}\n")
        f.write("\n")
        
        # Write relationships section
        f.write("Relationships (Shared Entities):\n")
        # Sort edges for consistent output
        edges = sorted(G.edges(data=True), key=lambda x: (x[0], x[1]))
        for domain1, domain2, data in edges:
            f.write(f"\n{domain1} <-> {domain2}:\n")
            for entity in sorted(data['shared_entities']):
                f.write(f"  - {entity}\n")

def main():
    """Main execution function"""
    try:
        G = create_domain_entity_graph(INPUT_PATH)
        visualize_graph(G, OUTPUT_DIR / "domain_relationships.png")
        export_graph_data(G, OUTPUT_DIR / "domain_relationships.txt")
        print("Graph generation completed successfully.")
    except Exception as e:
        print(f"Error generating graph: {str(e)}")

if __name__ == "__main__":
    main()