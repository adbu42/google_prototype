from thefuzz import fuzz, process

search_input = 'uts Australia'

print(f'you searched for "{search_input}"')

url_id_mapping = './WebbSpam/url_id_mapping'

url_map = {}
with open(url_id_mapping, 'r') as f:
    for line in f:
        node_id, url = line.strip().split()
        url_map[url] = node_id

print(process.extract(search_input, url_map.keys(), limit=100, scorer=fuzz.partial_ratio))
