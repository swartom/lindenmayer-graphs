#!/usr/bin/env python3

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
# l = list()
# for f in open("exec.txt"):
#     l.append(int(f.split(" ")[1]))


import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
graph = 10 ** 4

plt.rcParams["font.family"] = "monospace"

fig = plt.figure(2)

ax2 = fig.add_subplot(1,1,1)

cmd = f"./sf {graph} {1} {4} {.5}"
os.system(cmd)

G = nx.read_adjlist("graph.adjlist")

g = G.to_undirected()
print(g)

degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
ax2.loglog(degrees, degree_freq ,marker="s",ms=2.5,mew=2,lw =0.0, c='g',label=f'Lindenmayer Graph')


g = nx.barabasi_albert_graph(graph,1)
g = g.to_undirected()
print(g)

degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
ax2.loglog(degrees, degree_freq ,marker=".",ms=2.5,mew=2,lw =0.0, c="r", label=f'Barabasi Albert')

plt.legend()
plt.savefig("ba_v_lg_plot.pdf")
ax2.set_xlabel("Degree")
ax2.set_ylabel("Frequency")
plt.show()
