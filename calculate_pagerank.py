import networkx as nx

# Define file paths
url_id_mapping = './WebbSpam/url_id_mapping'
url_graph_file = './WebbSpam/url_graph_file'
host_id_mapping = './WebbSpam/host_id_mapping'
host_graph_file = './WebbSpam/host_graph_file'
url_with_redirects_graph_file = './WebbSpam/url_with_redirects_graph_file'

# create a directed graph
G = nx.DiGraph()

# Read in host graph
with open(host_graph_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        source = nodes[0]
        targets = nodes[1:]
        for target in targets:
            G.add_edge(source, target)

# Read in URL graph
with open(url_graph_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        source = nodes[0]
        targets = nodes[1:]
        for target in targets:
            G.add_edge(source, target)

# Read in host id mapping
host_map = {}
with open(host_id_mapping, 'r') as f:
    for line in f:
        node_id, host = line.strip().split()
        host_map[node_id] = host

# Read in URL id mapping
url_map = {}
with open(url_id_mapping, 'r') as f:
    for line in f:
        node_id, url = line.strip().split()
        url_map[node_id] = url

# Apply PageRank algorithm
pr = nx.pagerank(G)

# Sort the results in descending order based on the PageRank values
sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)

# Open a file for writing the results
with open("pagerank_results.txt", "w") as f:
    # Print min and max of PR results
    min_pr = min(pr.values())
    max_pr = max(pr.values())
    f.write(f"Maximum PageRank: {max_pr:.8f}\n")
    f.write(f"Minimum PageRank: {min_pr:.8f}\n")

    f.write("Node ID\tURL\tPageRank\n")

    # Print results
    for node_id, pr_value in sorted_pr:
        f.write(f"Node: {node_id}, URL: {url_map[node_id]}, PageRank: {pr_value:.8f}\n")
