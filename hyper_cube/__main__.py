#!/usr/bin/env python3


threads = [1,2,4,6,12]
repeats = 4
if __name__ == '__main__':
    print("Building Figures for HYPER_CUBE")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -Ofast -lm -pthread ./hyper_cube/hyper_cube.c -o hc"
    os.system(cmd)
    # for this binary the first module is the order of the graph, the second
    # is the threads
    import time
    for _ in range(repeats):
        datapoint =list()
        for i in threads:

            cmd = f"./hc 22 {i}"
            os.system(cmd)
            result = os.popen(cmd).read()

            datapoint.append((float(result.split('s')[0].split('\n')[1]),i))

        plt.plot(datapoint)
    plt.show()
