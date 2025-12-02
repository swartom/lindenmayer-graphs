#!/usr/bin/env python3

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
# l = list()
# for f in open("exec.txt"):
#     l.append(int(f.split(" ")[1]))


G = nx.read_adjlist("graph.adjlist")


g = G.to_undirected()
print(g)

degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)



plt.rcParams["font.family"] = "monospace"

fig = plt.figure(2)

ax2 = fig.add_subplot(1,1,1)
# axins = ax2.inset_axes(
#     [0.55, 0.15, 0.4, 0.2],
#     xlim=(10^1 , 20), ylim=(10**3 * 2, 10**4  * 3))

degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))

ax2.loglog(degrees, degree_freq,c="red",marker=".",ms=2.5,mew=2,lw =0.5, label=f'p=0.75')

plt.show()
