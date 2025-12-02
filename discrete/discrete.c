#include "discrete.h"
#include <gsl/gsl_rng.h>
#include <pthread.h>
#include <time.h>



typedef struct parametric_module {
    void * previous;
    uint8_t kind;
    INTEGER_TYPE x;
    INTEGER_TYPE y;
} module;

typedef struct wrapper {
    module* m;
} w;

module* restrict pre_allocation;

void* rule( void* p) {
    #define M ((w *)p)->m

    module* elements = (module*) &pre_allocation[( ((M->y) - (M->x))/DIVISOR + M->x - 1)];
    #define A_r elements[0]

    A_r.kind = 'A';
    A_r.x = M->x;
    A_r.y = ((M->y) - (M->x))/DIVISOR + M->x; // r-1
    A_r.previous = M->previous;
    M->previous = &A_r;
    M->x = A_r.y + 1;
    #define check_M if (M->x != M->y) rule(p);

    if (A_r.x != A_r.y){
        w wrapper;
        wrapper.m = &A_r;
        if((A_r.y)-(A_r.x) > (LIMIT) ){
            pthread_t thread;
            pthread_create( &thread, NULL, rule, &wrapper);
            check_M
            pthread_join(thread,NULL);
        } else {
            rule(&wrapper);
            check_M
        }
    } else check_M
    return 0;
}

int write_file(module* iv) {
    module* chain = iv;
    FILE *fptr;
    fptr = fopen("graph.adjlist", "w");
    /* fprintf(fptr, "graph {\nnode[shape=point]"); */
    int test = 0;
    do {
        switch (chain->kind) {
            case 'A':
                if( test++ == 0)
                    fprintf(fptr, "%d ",chain->x);
                else
                    fprintf(fptr, "\n%d",chain->x);
                    /* fprintf(fptr, "}\nnode[shape=point]\n%d -- {",chain->x); */
                break;
            default:
                fprintf(fptr, " %d",chain->x);
                break;
        }
        chain = chain->previous;
    }while (chain != NULL);
    /* fprintf(fptr, "}\n }"); */
    fclose(fptr);
    return 0;
}

int write_dot_file(module* iv) {
    module* chain = iv;
    FILE *fptr;
    fptr = fopen("graph.dot", "w");
    fprintf(fptr, "graph {repulsiveforce=.2\n\nbeautify=false \n \nnode[shape=point,width=.001,color=\"maroon\"]\nedge[penwidth=0.01,color=\"gray\"]");
    int test = 0;
    do {
        switch (chain->kind) {
            case 'A':
                if( test++ == 0)

                    /* fprintf(fptr, "%d ",chain->x); */
                    fprintf(fptr, "%d -- {",chain->x);
                else
                    /* fprintf(fptr, "\n%d",chain->x); */
                    fprintf(fptr, "}\n%d -- {",chain->x);
                break;
            default:
                fprintf(fptr, " %d",chain->x);
                break;
        }
        chain = chain->previous;
    }while (chain != NULL);
    fprintf(fptr, "}\n }");
    fclose(fptr);
    return 0;
}


int main(int argc, char *argv[]) {
    

    sscanf(argv[1],"%d", &MAX);
    sscanf(argv[2],"%d", &THREADS);


    double total = 0.0;
    double* times = alloca(REPETITIONS*sizeof(double));
    for(int i = 0; i < REPETITIONS; i ++){
    INTEGER_TYPE max = MAX;
    module* iv = (module*)malloc(sizeof(module));
    iv->kind = 'A';
    iv->x = 1;
    iv->y = max;

    w wrapper;
    wrapper.m = iv;

    pre_allocation = (module *)malloc(sizeof(module)*(MAX));
    
    struct timespec start={0,0}, end={0,0};
    sleep(SECONDS_WAIT_BETWEEN_REPEATS);

    clock_gettime(CLOCK_MONOTONIC, &start);
    rule(&wrapper);
    clock_gettime(CLOCK_MONOTONIC, &end);
    times[i] = (end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec);
    total += times[i];
    /* printf("%.10fs\n",((end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec))); */

    /* if (REPETITIONS == 1) */
    /*     write_dot_file(iv); */

    /* module* previous = iv; */
    /* do { */
    /*     iv = iv->previous; */
    /*     switch (iv->kind) { */
    /*         case 'A': */
    /*             free(previous); */
    /*             previous = iv; */
    /*     } */
    /* }while (previous->x != 1); */
    /* free(previous); */
    free(pre_allocation);
    free(iv);
    }


    double average = total/(double)(REPETITIONS);
    /* double sum = 0; */
    /* for (int i = 0; i < REPETITIONS; ++i) */
    /*     sum += pow(times[i] -average,2); */
    /* double variance = sum/REPETITIONS; */
    /* double std_deviation = sqrt(variance); */
    /* printf("Edges: %d10\n",(MAX*CONNECTIONS)); */
    printf("%.10fs\n", average);
    /* printf("%.2fmE/PE/s",(((double)(MAX*CONNECTIONS)/1000000)/PROCESSORS)/average); */
    return 1;
}
