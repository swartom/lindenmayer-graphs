#!/usr/bin/env python3


data = dict()

import os
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
os.system(cmd)
import numpy as np
keys = []
threads = [2**(i+5) for i in range(4)]
graphs = range(2,8)
options= [ 10**(i) for i in graphs]
headers = [ f'10^{i}' for i in graphs]
edges=  [2**(i+2) for i in range(4)]
for a in edges:
    print(f"Count: {a}")
    for edge in threads:
        print(f"Edges: {edge}")
        datapoint =list()
        for i in options:
            cmd = f"./sf {i} {edge} {a} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()


            result =  result.split("\n")
            from scipy import stats

            import statistics
            import pandas as pd

            array = [float(r) for r in result if r != "" ]
            import pandas as pd
            import numpy as np
            from scipy import stats

            df = pd.DataFrame(array)

            df = df[(np.abs(stats.zscore(df)) < 1).all(axis=1)]
            array = [float(f) for f in df.to_numpy()]
            print(array)


            # df = pd.DataFrame(data)
            # df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]



            geo = statistics.geometric_mean(array)
            sd = statistics.stdev(array)
            datapoint.append(f'${geo*1000:.1f}ms\\pm {(sd/geo)*100:.1f}\\% ({len(array)})$')
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
