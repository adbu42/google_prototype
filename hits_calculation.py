import networkx as nx
import matplotlib.pyplot as plt

url_graph_file = 'TestDataset/url_graph_file'
url_id_mapping = 'TestDataset/url_id_mapping'

G = nx.DiGraph()

# Read in URL id mapping
url_map = {}
with open(url_id_mapping, 'r') as f:
    for line in f:
        node_id, url = line.strip().split()
        url_map[node_id] = url

# Read in URL graph
with open(url_graph_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        source = nodes[0]
        targets = nodes[1:]
        for target in targets:
            G.add_edge(url_map[source], url_map[target])

pr = nx.hits(G)
hubs = pr[0].items()
authority = pr[1].items()

with open("hits_results.txt", "w") as f:
    # Print min and max of PR results
    f.write("Node ID\tHub\tAuthority\n")

    # Print results
    for hub_value, auth_value in zip(hubs, authority):
        f.write(f"Node: {hub_value[0]}, Hubs: {hub_value[1]:.8f}, Authority: {auth_value[1]:.8f}\n")
