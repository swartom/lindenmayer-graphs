#!/usr/bin/env python3


threads = [i for i in range(1,110,10)]
repeats = 1
graph= 2_500_000
if __name__ == '__main__':
    print("Building Figures for The Scale-free graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
    os.system(cmd)

    import time
    for a in range(repeats):
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"taskset -c 0-{i-1} ./sf {graph*i} {4} {200} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,total))
        import numpy as np
        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        plt.plot(x,y,marker='x')
        # plt.scale('log')
    plt.xlabel("threads")
    plt.ylabel("execution-time")
    plt.savefig('output.pdf')
