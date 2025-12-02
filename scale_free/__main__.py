#!/usr/bin/env python3


threads = [1,2,4,8,16,32,64]
repeats = 1
graph= 250_000_000
if __name__ == '__main__':
    print("Building Figures for The Scale-free graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
    os.system(cmd)
    import numpy as np
    w = open("data.txt","w")
    for a in range(repeats):
        print(a)
        datapoint =list()
        for i in threads:
            cmd = f"./sf {graph} {4} {i} {0.50}"
            os.system(cmd)
            result = os.popen(cmd).read()
            total = float(result.split('s')[0])
            datapoint.append((i,((graph*4)/total)/10**6))
            print(f"{i},{total}")
        w.write(f"{datapoint}\n")
        data = np.array(datapoint)
        x = data[:,0]
        y = data[:,1]
        plt.plot(x,y,marker='x')

    ideal_point = data[0]
    data = list()
    for i in threads:
        data.append((i,i*ideal_point[1]))
    data = np.array(data)
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,'--g')
    plt.xlabel("Nodes")
    plt.ylabel("Rate (Million Edges/Second)")
    plt.savefig('output.pdf')
