#!/usr/bin/env python3

import networkx as nx
import time
a = time.time_ns()
nx.hypercube_graph(17)
b = time.time_ns()
print((b-a)/10**9)
