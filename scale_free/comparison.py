#!/usr/bin/env python3

import numpy as np

# find how many times can pythons networkx construct a
# 1 edge power-law graph in?

import networkx as nx

repetitions = 1

import time
size = 10**6
then = time.time()
nx.barabasi_albert_graph(size,1)
now = time.time()

limit = now - then
keys = []
threads = [4]
graphs = range(6,9)
options= [ 10**(i) for i in graphs]
headers = [ f'10^{i}' for i in graphs]
edges=  [1]

data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
import numpy as np

for a in edges:
    print(f"Count: {a}")
    for edge in threads:
        print(f"Edges: {edge}")
        datapoint =list()
        for i in options:
            total = 0
            count = 0
            while(total < limit):
                count += 1
                cmd = f"./sf {i} {a} {edge} {0.50}"
                os.system(cmd)
                result = os.popen(cmd).read()
                total += float(result.split('s')[0])
            datapoint.append(f'{count} ({total/count:.2f}s/pg)')
        key = f'${limit:.2f}s$'
        data[key] = datapoint
        keys.append(key)

textabular = f"r||{'r'*len(headers)}"
texheader = " & $" + "$ & $".join(headers) + "$\\\\"
texdata = "\\hline\n"
for label in keys:
    const = map(str,data[label])
    texdata += f"{label} & {' & '.join(const)} \\\\\n"


print("\\begin{tabular}{"+textabular+"}")
print(texheader)
print(texdata,end="")
print("\\end{tabular}")
