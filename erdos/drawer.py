#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
import networkx as nx
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./erdos/erdos.c -o er"
os.system(cmd)
size = 2500
cmd = f"./er {size} {0.1} "
os.system(cmd)
G = nx.read_adjlist(f"graph.adjlist")
g = G.to_undirected()



degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
plt.loglog(degrees, degree_freq,marker="s",c="g")

import networkit as nk

erg = nk.generators.ErdosRenyiGenerator(size, 0.1)
ergG = erg.generate()

G = nk.nxadapter.nk2nx(ergG)
g = G.to_undirected()



degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
plt.loglog(degrees, degree_freq,marker="x",c="r")
plt.xlim(10**2)


G = nx.erdos_renyi_graph(size,0.1)
g = G.to_undirected()



degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
plt.loglog(degrees, degree_freq,marker=".",c="b")
plt.show()
