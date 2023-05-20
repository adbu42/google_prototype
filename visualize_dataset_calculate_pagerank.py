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

nx.draw(G, with_labels=True)
plt.show()

pr = nx.pagerank(G)
sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)

with open("pagerank_results.txt", "w") as f:
    # Print min and max of PR results
    min_pr = min(pr.values())
    max_pr = max(pr.values())
    f.write(f"Maximum PageRank: {max_pr:.8f}\n")
    f.write(f"Minimum PageRank: {min_pr:.8f}\n")

    f.write("Node ID\tPageRank\n")

    # Print results
    for node_id, pr_value in sorted_pr:
        f.write(f"Node: {node_id}, PageRank: {pr_value:.8f}\n")
