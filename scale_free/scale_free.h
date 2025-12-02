#ifndef SCALE_FREE_H_
#define SCALE_FREE_H_

#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <stdio.h>
#include <unistd.h>

int MAX = 1000;
#define DIVISOR 2
int CONNECTIONS = 4;
int THREADS =  64;  // (uint32_t)sysconf(_SC_NPROCESSORS_ONLN) * 8
#define LIMIT (MAX/(2*THREADS))
#define REPETITIONS 10
#define SECONDS_WAIT_BETWEEN_REPEATS 0

// System Info
#define INTEGER_TYPE uint64_t
#define SEED 150

int ALPHA = 0.5;
#define BETA 1.0

#define A 1
#define C 1
#define MAX_PERIOD A_r.y

#endif // SCALE_FREE_H_2
