
threads = [2,4,8,16,32]
repeats = 1
graph= 250_000
if __name__ == '__main__':
    print("Building Figures for The Scale-free graph")
    import os
    import matplotlib.pyplot as plt
    cmd = "gcc -lcblas -lgsl -O3 -lm -pthread ./scale_free/scale_free.c -o sf"
    os.system(cmd)
    import numpy as np
    datapoint =list()
    for i in [0.0625,0.125,0.25,0.375,0.50,0.625,0.75,0.875]:
        cmd = f"./sf {graph} {4} {32} {i}"
        os.system(cmd)
        result = os.popen(cmd).read()
        total = float(result.split('s')[0])
        datapoint.append((i,total))

    data = np.array(datapoint)
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,marker='x')
    plt.ylim(0,1)
    plt.savefig('output.pdf')
