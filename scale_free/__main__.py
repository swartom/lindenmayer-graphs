#!/usr/bin/env python3
threads = [1,2,4,8,16,32]  # 1,2,4,
repeats = 1
graph= 100_000_000#_000# 1_000_000#_000
if __name__ == '__main__':
    print("Building Figures for The Scale-free graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
    os.system(cmd)
    import numpy as np

    edges = 3
    for a in range(repeats):

        datapoint =list()
        for i in threads:
            cmd = f"./sf {graph} {edges} {i} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            print(result)
            total = float(result.split('s')[0])
            print(total,result.split('s')[0])
            datapoint.append((i,total))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        z = y/x
        y = y[0]/y
        plt.figure(1)
        plt.plot(x,z,'b',marker='x')
        plt.xlabel("Threads")
        plt.ylabel("Rate (Million particles connections/second/ Processor)")
        plt.savefig('out1.pdf')
        plt.figure(2)
        plt.plot(x,y,'r',marker='x')
        plt.savefig('strong_scaling.pdf')
        plt.figure(3)
    ideal_point = data[0]
    graph = graph//threads[-1]
    for a in range(repeats):
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"./sf {graph*i} {edges} {i} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,total))
            print(f"{i},{total}")

        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]

        plt.plot(x,y,'g',marker='o')
    plt.xlabel("Threads")
    plt.ylabel("Seconds")
    plt.savefig('weak_scaling.pdf')
