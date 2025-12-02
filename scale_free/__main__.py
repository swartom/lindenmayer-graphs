#!/usr/bin/env python3


threads = [2,4,8,16,32]
repeats = 1
graph= 250_000_000
if __name__ == '__main__':
    print("Building Figures for The Scale-free graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
    os.system(cmd)
    import numpy as np

    cmd = f"./sf {graph} {4} {1} {0.50}"
    os.system(cmd)
    result = os.popen(cmd).read()
    comparison = float(result.split('s')[0])

    for a in range(repeats):
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"./sf {graph} {60} {i} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,comparison/total))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        plt.plot(x,y,marker='x')
        plt.xscale('log')
    plt.xlabel("threads")
    plt.ylabel("speed-up")
    plt.savefig('output.pdf')
