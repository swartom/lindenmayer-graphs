import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
# l = list()
# for f in open("exec.txt"):
#     l.append(int(f.split(" ")[1]))


import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./erdos/erdos.c -o er"
os.system(cmd)
n= 10**4
cmd = f"./er {n} {1/(n-1)}"

os.system(cmd)


import networkx as nx

import matplotlib.pyplot as plt

G = nx.read_adjlist("graph.adjlist")
nx.draw(G,node_size=1,node_color="red")

plt.show()
plt.savefig("Erdosgraph.pdf")
