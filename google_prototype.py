import networkx as nx
from thefuzz import fuzz, process
import argparse

# Define file paths
url_id_mapping = './WebbSpam/url_id_mapping'
url_graph_file = './WebbSpam/url_graph_file'
url_with_redirects_graph_file = './WebbSpam/url_with_redirects_graph_file'

# get the search input
parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Search in websites with pagerank. Remember to put multiple keywords in parenthesis"
    )
parser.add_argument("-s", "--search", required=True)
args = parser.parse_args()
search_input = args.search
print(f'you searched for "{search_input}":')

# create a directed graph
G = nx.DiGraph()

# Read in URL id mapping
url_map = {}
with open(url_id_mapping, 'r') as f:
    for line in f:
        node_id, url = line.strip().split()
        url_map[node_id] = url
        G.add_node(node_id)

# Read in URL graph
with open(url_graph_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        source = nodes[0]
        targets = nodes[1:]
        for target in targets:
            G.add_edge(source, target)

# Apply PageRank algorithm
pr = nx.pagerank(G)

# Search for the keywords
search_results = dict(process.extract(search_input, url_map.values(), limit=100, scorer=fuzz.partial_ratio))

# Add the pagerank results to the similarity ranking of the search. The search results are between 0 and 100. The
# pagerank results are between 0 and 1, so a factor of 0.01 is applied to the search results. To give the pagerank value
# more significance, it is multiplied by 10.
for node_id, pr_value in pr.items():
    if url_map[node_id] in search_results.keys():
        search_results[url_map[node_id]] = search_results[url_map[node_id]] * 0.01 + pr_value * 10

# Sort the results in descending order based on the combined pagerank and search values
sorted_results = sorted(search_results.items(), key=lambda x: x[1], reverse=True)
for sorted_result in sorted_results[:10]:
    print(sorted_result[0])
