#!/usr/bin/env python3


data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
import numpy as np
keys = []
threads = [32]
graphs = range(3,7)
options= [ 10**(i) for i in graphs]
headers = [ f'10^{i}' for i in graphs]
edges=  [2**(i+1) for i in range(6)]
for a in edges:
    print(f"Count: {a}")
    for edge in threads:
        print(f"Edges: {edge}")
        datapoint =list()
        for i in options:
            cmd = f"./sf {i} {a} {edge} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            sd = float(result.split('s')[1])
            mepe = ((i*a)/total/edge)/10**6
            datapoint.append(f'{ "\\cellcolor{green}\\color{white} " if mepe > 27.65 else "" }${mepe:.1f}\\pm {(sd/total)*100:.2f}\\%$')
        key = f'$d={a}$'
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
