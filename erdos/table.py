#!/usr/bin/env python3


data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./erdos/erdos.c -o er"
os.system(cmd)
import numpy as np
keys = []
threads = [2,4,8,16,32]
graphs = range(1,4)
options= [ 10**(i) for i in graphs]
headers = [ f'10^{i}' for i in graphs]
edges=  [0.1,0.25,0.5,0.75,0.9]
for a in edges:
    print(f"Count: {a}")
    for edge in threads:
        print(f"Edges: {edge}")
        datapoint =list()

        for i in options:
            cmd = f"taskset -c 0-{edge-1} ./er {i} {a} "
            total = 0
            for _ in range(10):
                os.system(cmd)
                result = os.popen(cmd).read()
                total += float(result.split('s')[0])*1000
            datapoint.append(f'${(total/10):.2f}ms$')
        key = f'$c=0-{edge-1},d={a}$'
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
