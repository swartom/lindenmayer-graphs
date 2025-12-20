#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkit as nk
import time
import os
import numpy as np

ls= [ 10**i for i in range(1,5)]
ls = [ a*b for b in range(1,10) for a in ls  if a*b <= 4*10**4]
for _ in range(10):
    d_nk = []
    d = []
    for i in ls:
        n = time.time()
        erg = nk.generators.ErdosRenyiGenerator(i, 0.1)
        ergG = erg.generate()
        a = time.time()
        d_nk.append((i,a-n))

        cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./erdos/erdos.c -o er"
        os.system(cmd)
        cmd = f"./er {i} {0.1} "
        n = time.time()
        os.system(cmd)
        a = time.time()
        d.append((i,a-n))



    d.sort()
    d_nk.sort()
    data = np.array(d)
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,c="g",marker="s")
    data = np.array(d_nk)
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,c="r",marker="x")
plt.savefig("vsnetworkit.pdf")
plt.show()
