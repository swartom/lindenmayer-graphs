#!/usr/bin/env python3


data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
import numpy as np
keys = []
threads = [2**(i+4) for i in range(5)]
graphs = range(2,7)
options= [ 10**(i) for i in graphs]
headers = [ f'10^{i}' for i in graphs]
edges=  [2**(i+4) for i in range(4)]
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
            datapoint.append(f'${total*1000:.5f}\\pm {(sd/total)*100:.2f}\\%$')
        key = f'{edge}-{a}'
        data[key] = datapoint
        keys.append(key)

textabular = f"r||{'r'*len(headers)}"
texheader = " & $" + "$ & $".join(headers) + "$\\\\"
texdata = "\\hline\n"
for label in keys:
    if label.split('-')[1]=='1':
        texdata += '\\hline '
    texdata += f"{label} & {' & '.join(map(str,data[label]))} \\\\\n"
    if label.split('-')[1]=='1':
        texdata += '\\hline '

print("\\begin{tabular}{"+textabular+"}")
print(texheader)
print(texdata,end="")
print("\\end{tabular}")
