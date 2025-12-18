#!/usr/bin/env python3

import networkx as nx

import matplotlib.pyplot as plt

G = nx.read_addjlist("graph.adjlist")
nx.draw(G)

plt.show()
