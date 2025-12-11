#!/usr/bin/env python3


data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
import numpy as np
keys = []
threads = [2**(i+5) for i in range(1)]
graphs = 8
options= [ 10**(i+1) for i in range(1,graphs)]
headers = [ f'10^{i+1}' for i in range(1,graphs)]
edges=  [2**(i+1) for i in range(7)]
for a in threads:
    print(f"Count: {a}")
    for edge in edges:
        datapoint =list()
        for i in options:
            cmd = f"./sf {i} {edge} {a} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            sd = float(result.split('s')[1])
            datapoint.append(f'${total:.5f}\\pm {(sd/total)*100:.2f}$')
        key = f'{edge}-{a}'
        data[key] = datapoint
        keys.append(key)

textabular = f"l|{'r'*len(headers)}"
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
