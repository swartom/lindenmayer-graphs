import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
# l = list()
# for f in open("exec.txt"):
#     l.append(int(f.split(" ")[1]))


import os
import networkit as nk
import time
import matplotlib.pyplot as plt
cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./erdos/erdos.c -o er"
os.system(cmd)
ls= [ 10**i for i in range(1,5)]
# ls = [ a*b for b in range(1,10) for a in ls  if a*b <= 4*10**4]
probabilites = [0.1]
fig, da = plt.subplots(1,2)
i = 0
for p in probabilites:
    ax = da[i]
    i+=1
    for repeats in range(1):
        datapoint_nk = []
        datapoint = []
        for n in ls:
            # print("test")
            # n = time.time()
            # erg = nk.generators.ErdosRenyiGenerator(10**4, 0.1)
            # ergG = erg.generate()
            # a = time.time()
            # datapoint_nk.append((n,a-n))
            print("Appended")
            cmd = f"./er {n} {p} "
            n = time.time()
            os.system(cmd)
            a = time.time()

            datapoint.append((n,a-n))

        datapoint.sort()
        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        ax.set_yscale("log")
        ax.plot(x,y,marker='s',c="g")
        datapoint_nk.sort()
        data = np.array(datapoint_nk)
        x = data[:,0]
        y = data[:,1]
        ax.plot(x,y,marker='x',c="r")


plt.savefig("Erdosgraph.pdf")
