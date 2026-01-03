import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

import os

import time
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./hamiltonian/hamiltonian.c -o ht"
os.system(cmd)
size = 10000
p = 0.01
p_1 = ((p*(size*(size -1))/2) - (size + 1))/((size*(size -1))/2)
print(p_1)

cmd = f"./ht {size} {p_1}"
os.system(cmd)
G = nx.read_adjlist(f"graph.adjlist")
g = G.to_undirected()
print(g)

degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
plt.loglog(degrees, degree_freq,marker="s",c="g")

cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./erdos/erdos.c -o er"
os.system(cmd)

cmd = f"./er {size} {p} "
os.system(cmd)
G = nx.read_adjlist(f"graph.adjlist")
g = G.to_undirected()



degree_sequence = sorted((d for n, d in g.degree()), reverse=True)
dmax = max(degree_sequence)
degree_freq = nx.degree_histogram(g)
degrees = range(len(degree_freq))
plt.loglog(degrees, degree_freq,marker="s",c="b")
plt.xlim(3* 10**1)
plt.savefig("Hamiltonian_vs_random.pdf")
