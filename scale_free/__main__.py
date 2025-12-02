#!/usr/bin/env python3
threads = [1,2,4,8,16,32]
repeats = 1
graph= 2**20# 1_000_000#_000
if __name__ == '__main__':
    print("Building Figures for The Scale-free graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
    os.system(cmd)
    import numpy as np

    edges = 64
    for a in range(repeats):
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"./sf {graph} {edges} {i} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,((graph*edges)/total)/10**6))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        z = y/x
        plt.figure(1)
        plt.plot(x,z,'b',marker='x')
        plt.xlabel("Threads")
        plt.ylabel("Rate (Million particles connections/second/ Processor)")
        plt.savefig('out1.pdf')
        plt.figure(2)
        plt.plot(x,y,'r',marker='x')
    ideal_point = data[0]
    data = list()
    for i in threads:
        data.append((i,i*(ideal_point[1])))
    data = np.array(data)
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,'--',color="0.5")
    graph = graph//threads[-1]
    for a in range(repeats):
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"./sf {graph*i} {edges} {i} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,(((graph*i*edges))/total)/10**6))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        plt.plot(x,y,'g',marker='o')
    plt.xlabel("Threads")
    plt.ylabel("Rate (Million particles connections/second)")
    plt.savefig('output.pdf')
