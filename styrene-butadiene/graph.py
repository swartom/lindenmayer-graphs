#!/usr/bin/env python3

import networkx as nx

import itertools as it
g = nx.MultiGraph()
connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.1] * 4)]
for line in open("graph.adjlist"):
    data = line.split(" ")
    g.add_node(data[0].strip())
    if len(data) > 1:
        for i in data[1:]:
            print(i)
            if i != "":
                g.add_edge(data[0],i.strip())

g.remove_node('')
nx.draw(g,pos = nx.kamada_kawai_layout(g)
,node_color="red",edge_color=".5",node_size=1,connectionstyle=connectionstyle)

import matplotlib.pyplot as plt


for i in g.edges:
    print(i)

plt.show()
