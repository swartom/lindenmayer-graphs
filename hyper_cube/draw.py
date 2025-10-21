#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
G = nx.read_adjlist("graph.adjlist")
print("readfile")
g = G.to_undirected()
g.remove_edges_from(nx.selfloop_edges(g))
print("undirected")
print(g)

# matrix = nx.convert_matrix(g)

fig = plt.figure(1)

subfigs = fig.subfigures(1, 2, wspace=0.07)

nx.draw(g,node_color="#B4111B",node_size=1,edge_color=".2")
plt.savefig('graph.pdf')
