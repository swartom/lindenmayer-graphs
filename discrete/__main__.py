#!/usr/bin/env python3
threads = [2,4,8,16,32]
graphs = [  i for i in range(1,10) ]
repeats = 1
if __name__ == '__main__':
    print("Building Figures for The Discrete graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -O3 -lm -pthread ./discrete/discrete.c -o ds"
    os.system(cmd)
    import numpy as np
    for a in threads:
        print(a)
        datapoint =list()
        for i in graphs:
            cmd = f"./sf {10 ** i} {4} {a} {0.5}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((10**i,total))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]

        plt.figure(1)
        plt.plot(x,y,marker='x',label=f'{a} Threads')
        # plt.legend()

    plt.xlabel("Graph  Vertices")
    plt.ylabel("Execution Time (seconds)")
    plt.xscale("log")
    plt.legend()
    plt.savefig('discrete_graph_execution_time.pdf')
