import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

import os

import time
import matplotlib.pyplot as plt

cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./hamiltonian/hamiltonian.c -o ht"
os.system(cmd)
size = 10**4

p = 0.01
propabilities = [(i+1)*p for i in range(10) ]
import random
for _ in range(10):
    data = []
    for p in propabilities:
        p_1 = ((p*(size*(size -1))/2) - (size + 1))/((size*(size -1))/2)
        print(p_1)

        cmd = f"./ht {size} {p_1} {random.randint(0,2**32)}"
        os.system(cmd)
        G = nx.read_adjlist(f"graph.adjlist")
        g = G.to_undirected()
        tsp = nx.approximation.traveling_salesman_problem
        SA_tsp = nx.approximation.simulated_annealing_tsp
        method = lambda G, weight: SA_tsp(G, "greedy", weight=weight, temp=500)
        path = tsp(G, cycle=False, method=method)
        print("Calibration Error: ", len(path)-size)
        data.append((p,len(path)-size))

    data = np.array(data)
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,marker='s')
plt.savefig("tspProblem.pdf")
plt.show()
