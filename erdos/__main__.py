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
ls= [ 10**i for i in range(1,5)]
ls = [ a*b for b in range(1,10) for a in ls  if a*b <= 5*10**4]
probabilites = [0.001,0.01]
fig, da = plt.subplots(1,2)
i = 0
for p in probabilites:
    ax = da[i]
    i+=1
    for repeats in range(10):
        datapoint = []
        for n in ls:
            cmd = f"./er {n} {p}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])

            datapoint.append((n,total))

        datapoint.sort()
        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        ax.set_yscale("log")
        ax.plot(x,y,marker='x')


plt.savefig("Erdosgraph.pdf")
