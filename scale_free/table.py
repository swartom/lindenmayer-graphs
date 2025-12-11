#!/usr/bin/env python3


data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
import numpy as np
keys = []
threads = [32]
graphs = range(1,9)
options= [ 10**(i) for i in graphs]
headers = [ f'10^{i}' for i in graphs]
edges=  [2**(i+1) for i in range(5)]
for a in edges:
    print(f"Count: {a}")
    for edge in threads:
        print(f"Edges: {edge}")
        datapoint =list()
        for i in options:
            cmd = f"./sf {i} {edge} {a} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            sd = float(result.split('s')[1])
            datapoint.append(f'${((i*a)/total/a)/10**6:.2f}ME/PU\\pm {(sd/total)*100:.2f}\\%$')
        key = f'$d={a}$'
        data[key] = datapoint
        keys.append(key)

textabular = f"r||{'r'*len(headers)}"
texheader = " & $" + "$ & $".join(headers) + "$\\\\"
texdata = "\\hline\n"
for label in keys:
    constr = map(str,data[label])
    const = [ "\\cellcolor{green} "+r if float(r) > 27 else r for r in constr]
    texdata += f"{label} & {' & '.join(const)} \\\\\n"


print("\\begin{tabular}{"+textabular+"}")
print(texheader)
print(texdata,end="")
print("\\end{tabular}")
