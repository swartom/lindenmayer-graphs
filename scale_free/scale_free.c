#include "scale_free.h"
#include <gsl/gsl_rng.h>
#include <gsl/gsl_cdf.h>
#include <pthread.h>
#include <time.h>



typedef struct parametric_module {
    void * previous;
    uint8_t kind;
    INTEGER_TYPE x;
    INTEGER_TYPE y;
} module;


typedef struct thin_parametric_module {
    void * previous;
    uint8_t kind;
    INTEGER_TYPE x;
} thin_module;

typedef struct wrapper {
    module* m;
    gsl_rng* r;
} w;

module* restrict pre_allocation;


void* rule( void* p) {
    #define M ((w *)p)->m
    #define R ((w *)p)->r
    /* switch (m->kind) { */
    /*     case 'A': */
    // int r = ((m->y) - (m->x))/DIVISOR + m->x + 1;
    // // Defining this here requires a memory call. The line below explains is equivalent to this line.
    module* elements = (module*) &pre_allocation[(CONNECTIONS + 1)*( ((M->y) - (M->x))/DIVISOR + M->x - 1)];
    /* module* elements = (module *)malloc((CONNECTIONS + 1)*sizeof(module)); */

    #define A_r elements[0]

    A_r.kind = 'A';
    A_r.x = M->x;
    A_r.y = ((M->y) - (M->x))/DIVISOR + M->x; // r-1
    A_r.previous = M->previous;

    M->previous = &elements[CONNECTIONS];
    M->x = A_r.y + 1;

    {
        /* double source = gsl_ran_flat(R, 0.01, 0.99); */
        /* source = gsl_cdf_beta_Pinv(source,.5,1); */
        double source = gsl_ran_beta(R, ALPHA, 1);
        /* double source = gsl_ran_gaussian(r,1); */
        /* double source = gsl_ran_gamma(r, 20.0,1.0); */

        integer_type x = (a_r.y)*source;
        /* integer_type c = x > 1 ? x*source + 1 : 1; // this is only true if the vlaue of connections is greather than x */

        for(int i =1; i < connections+1; i++) {
            elements[i].kind = 'l';

            x = (integer_type)((a)*x + c) % (max_period);
            elements[i].previous = &elements[i-1];
            elements[i].x = x + 1; // because we index vertices from 1 not 0
         }
    }

    #define check_m if (m->x != m->y) rule(p);

    if (a_r.x != a_r.y){
        w wrapper;
        wrapper.m = &a_r;

        if((a_r.y)-(a_r.x) > (limit) ){
            /* printf("%d,%d,%d,%d\n",a_r.y,a_r.x, a_r.y - a_r.x,(limit + 1)); */
            pthread_t thread;
            wrapper.r = gsl_rng_alloc (gsl_rng_taus);
            gsl_rng_set(wrapper.r,seed+a_r.y);
            pthread_create( &thread, null, rule, &wrapper);
            check_m
            pthread_join(thread,null);
            gsl_rng_free(wrapper.r);
        } else {
            wrapper.r = r;
            rule(&wrapper);
            check_m
        }
    } else check_m
    return 0;
}

int write_file(module* iv) {
    module* chain = iv;
    file *fptr;
    fptr = fopen("graph.adjlist", "w");
    /* fprintf(fptr, "graph {\nnode[shape=point]"); */
    int test = 0;
    do {
        switch (chain->kind) {
            case 'a':
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
    }while (chain != null);
    /* fprintf(fptr, "}\n }"); */
    fclose(fptr);
    return 0;
}

int write_dot_file(module* iv) {
    module* chain = iv;
    file *fptr;
    fptr = fopen("graph.dot", "w");
    fprintf(fptr, "graph {repulsiveforce=.2\n\nbeautify=false \n \nnode[shape=point,width=.001,color=\"maroon\"]\nedge[penwidth=0.01,color=\"gray\"]");
    int test = 0;
    do {
        switch (chain->kind) {
            case 'a':
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
    }while (chain != null);
    fprintf(fptr, "}\n }");
    fclose(fptr);
    return 0;
}


int main(int argc, char *argv[]) {


    sscanf(argv[1],"%d", &max);
    sscanf(argv[2], "%d", &connections);
    sscanf(argv[3],"%d", &threads);

    sscanf(argv[4], "%lf", &alpha);
    
    double total = 0.0;
    double* times = alloca(repetitions*sizeof(double));
    for(int i = 0; i < repetitions; i ++){
    gsl_rng *rand_src;
    rand_src = gsl_rng_alloc (gsl_rng_taus);

    integer_type max = max;
    module* iv = (module*)malloc(sizeof(module));
    iv->kind = 'a';
    iv->x = 1;
    iv->y = max;

    w wrapper;

    wrapper.m = iv;
    wrapper.r = rand_src;
    gsl_rng_set(wrapper.r,seed);

    pre_allocation = (module *)malloc((connections + 1)*sizeof(module)*max);
    
    struct timespec start={0,0}, end={0,0};
    sleep(seconds_wait_between_repeats);

    clock_gettime(clock_monotonic, &start);
    rule(&wrapper);
    clock_gettime(clock_monotonic, &end);
    times[i] = (end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec);
    total += times[i];
    /* printf("%.10fs\n",((end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec))); */

    /* if (repetitions == 1) */
    /*     write_file(iv); */

    /* module* previous = iv; */
    /* do { */
    /*     iv = iv->previous; */
    /*     switch (iv->kind) { */
    /*         case 'a': */
    /*             free(previous); */
    /*             previous = iv; */
    /*     } */
    /* }while (previous->x != 1); */
    /* free(previous); */
    free(pre_allocation);
    free(iv);
    gsl_rng_free(rand_src);
    }

    double average = total/(double)(repetitions);
    /* double tot = times[0]; */
    /* printf("%f\n",tot); */
    /* for(int i = 0; i < repetitions; ++i){ */
    /*     printf("%lf\n",times[i]); */
    /* } */
    /* average = pow(1/REPETITIONS,tot); */
    double sum = 0;
    for (int i = 0; i < REPETITIONS; ++i)
        sum += pow(times[i] -average,2);
    double variance = sum/REPETITIONS;
    double std_deviation = sqrt(variance);

    /* printf("Edges: %d10\n",(MAX*CONNECTIONS)); */
    printf("%.10fs%.10f\n", average,std_deviation);
    /* printf("%.2fmE/PE/s",(((double)(MAX*CONNECTIONS)/1000000)/PROCESSORS)/average); */
    return 1;
}
