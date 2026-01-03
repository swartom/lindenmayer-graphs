#ifndef HAMILTONIAN_H_
#define HAMILTONIAN_H_

#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <stdio.h>
#include <unistd.h>

#include <pthread.h>
#include <time.h>

#define INTEGER_TYPE uint32_t

typedef struct parametric_module {
    void * previous;
    uint8_t kind;
    INTEGER_TYPE x;
    INTEGER_TYPE y;
} module;

#endif // HAMILTONIAN_H_
