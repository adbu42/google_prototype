import networkx as nx
from urllib.parse import urlparse

# Define file paths
url_graph_file = './WebbSpam/url_graph_file'
url_with_redirects_graph_file = './WebbSpam/url_with_redirects_graph_file'
url_id_mapping = './WebbSpam/url_id_mapping'

# Read URLs and extract full URLs
url_full_urls = {}
with open(url_id_mapping, 'r') as f:
    for line in f:
        node_id, url = line.strip().split()
        try:
            url_full_urls[node_id] = url
        except ValueError:
            pass

# Enter the target domain to search
target_domain = input("Enter the target domain to search: ")

# Create a directed graph
G = nx.DiGraph()

# Read in URL graph and filter URLs by target domain
with open(url_graph_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        source = nodes[0]
        targets = nodes[1:]
        source_url = url_full_urls.get(source)
        if source_url:
            try:
                source_domain = urlparse(source_url).netloc
                if source_domain == target_domain:
                    G.add_node(source, label=source_url)
                    for target in targets:
                        target_url = url_full_urls.get(target)
                        if target_url and target_url != source_url:
                            try:
                                target_domain_inner = urlparse(target_url).netloc
                                if target_domain_inner == target_domain:
                                    G.add_edge(source, target)
                            except ValueError:
                                pass
            except ValueError:
                pass

# Read in URL graph with redirects
with open(url_with_redirects_graph_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        source = nodes[0]
        targets = nodes[1:]
        source_url = url_full_urls.get(source)
        if source_url:
            try:
                source_domain = urlparse(source_url).netloc
                if source_domain == target_domain:
                    G.add_node(source, label=source_url)
                    for target in targets:
                        target_url = url_full_urls.get(target)
                        if target_url and target_url != source_url:
                            try:
                                target_domain_inner = urlparse(target_url).netloc
                                if target_domain_inner == target_domain:
                                    G.add_edge(source, target)
                            except ValueError:
                                pass
            except ValueError:
                pass

# Create an output file in Gephi format
output_file = f'{target_domain}.gexf'
nx.write_gexf(G, output_file, version='1.2draft')

# Count the nodes and edges
node_count = G.number_of_nodes()
edge_count = G.number_of_edges()

# Print the total count of nodes and edges
print(f"\nGraph with nodes from domain '{target_domain}' has been saved to {output_file}.")
print(f"Total Nodes: {node_count}")
print(f"Total Edges: {edge_count}")
