#!/usr/bin/env python3
threads = [1,2,4,8,16,32]
graphs = [ 10 ** i for i in range(1,6) ]
repeats = 1
if __name__ == '__main__':
    print("Building Figures for The Discrete graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -O3 -lm -pthread ./discrete/discrete.c -o ds"
    import numpy as np
    for a in graphs:
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"./ds {a} {i}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,((a)/total)/10**6))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]

        plt.figure(1)
        plt.plot(x,y,'b',marker='x')
    plt.savefig('discrete_graph_execution_time.pdf')
