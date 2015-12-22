import networkx as nx
import csv, json

import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from([1], donor="Chi-An")
G.add_nodes_from([2], donor="James")
G.add_nodes_from([3], donor="Sirui")

G.add_edges_from([(1,3), (1,2)], color="blue")
G[1][2]["weight"] = 9.2


G.number_of_nodes()

G.number_of_nodes()

random_layout = nx.random_layout(G)
nx.draw_networkx_nodes(G, random_layout, node_color="blue", node_size=200, alpha=0.6)

nx.draw(G)
plt.show()