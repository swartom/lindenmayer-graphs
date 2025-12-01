#!/usr/bin/env python3

if __name__ == '__main__':
    print("Building Figures for HYPER_CUBE")
    import os
    os.system("gcc -Ofast -lm -pthread ./hyper_cube/hyper_cube.c -o hc")
