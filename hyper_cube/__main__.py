#!/usr/bin/env python3


values = [i+1 for i in range(24)]
threads = [0,1,2,3]

if __name__ == '__main__':

    print("Building Figures for HYPER_CUBE")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -Ofast -lm -pthread ./hyper_cube/hyper_cube.c -o hc"
    os.system(cmd)
    # for this binary the first module is the order of the graph, the second
    # is the threads
    import time

    for j in threads:
        datapoint =list()
        for i in values:

            cmd = f"./hc {i} {j}"
            os.system(cmd)
            result = os.popen(cmd).read()
            datapoint.append((float(result.split('s')[0].split('\n')[1]),i))

        import numpy as np

        data = np.array(datapoint)
        x = data[:,1]
        y = data[:,0]

        plt.plot(x,y,label=f"{3**j}")

    plt.legend()
    plt.xlabel("Order")
    plt.yscale("log")
    plt.ylabel("Seconds")
    plt.savefig("hyper_cube.pdf")
