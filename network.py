# Data Source: https://snap.stanford.edu/data/wikispeedia.html
# Other sources used:
# https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#reading-files-importing-data
# Libraries used:
# https://networkx.org/documentation/stable/tutorial.html

import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.

node_path = "./wikispeedia_paths-and-graph/articles.tsv"
edge_path = "./wikispeedia_paths-and-graph/links.tsv"

with open(node_path, 'r') as tsv_file: # Open the file
    nodereader = csv.reader(tsv_file, delimiter="\t") # Read the csv
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][12:]

node_names = [n[0] for n in nodes] # Get a list of only the node names

with open(edge_path, 'r') as edgetsv: # Open the file
    edgereader = csv.reader(edgetsv, delimiter="\t") # Read the csv
    edges = [tuple(e) for e in edgereader][12:] # Retrieve the data

G = nx.DiGraph()
for n in node_names:
    G.add_node(n, article=n)
G.add_edges_from(edges)

print(nx.info(G))

# print(list(G.adj["Orca"]))
# print(G.nodes["Orca"])

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

def bfs(graph, source, target):
    queue = []
    visited = []
    parent = {}

    queue.append(source)
    visited.append(source)

    while queue:
        vertex = queue.pop(0)

        if G.nodes[vertex]["article"] == target:
            return backtrace(parent, source, target)

        for neighbor in list(graph.adj[vertex]):
            if neighbor not in visited:
                parent[neighbor] = vertex
                visited.append(neighbor)
                queue.append(neighbor)

print()
print(bfs(G, "Orca", "Kangaroo"))
print(bfs(G, "14th_century", "Fire"))
print(bfs(G, "Batman", "Jazz"))
print(bfs(G, "Edgar_Allan_Poe", "Zebra"))
print(bfs(G, "Achilles_tendon", "Ivory"))
print(bfs(G, "Planet", "Jimmy_Wales"))
