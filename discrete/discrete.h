#ifndef SCALE_FREE_H_
#define SCALE_FREE_H_

#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int MAX = 1000;
#define DIVISOR 2
int THREADS =  64;  // (uint32_t)sysconf(_SC_NPROCESSORS_ONLN) * 8
#define LIMIT (MAX/(2*THREADS))
#define REPETITIONS 1
#define SECONDS_WAIT_BETWEEN_REPEATS .5

// System Info
#define INTEGER_TYPE uint32_t
#define SEED 150

#endif // SCALE_FREE_H_2
