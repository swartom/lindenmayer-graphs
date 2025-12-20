#include "erdos.h"


int MAX = 0;
double P = 0.01;

#define LIMIT (MAX/((1.5)*THREADS))
#define THREADS 64

#define SEED 100

typedef struct wrapper {
    module* m;
    gsl_rng* r;
} w;


double c = 0;
module * restrict pre_alloc;
double get_random() { return (double)rand() / (double)RAND_MAX; }
void* rule( void* p) {
    #define M ((w *)p)->m
    #define R ((w *)p)->r
    uint32_t mid  = 3*((M->y) - (M->x))/4 + M->x; // r-1

    module* elements = (module*) &pre_alloc[(mid)*(MAX)];

    #define A_r elements[0]

    A_r.kind = 'A';
    A_r.x = M->x;
    A_r.y = mid;
    A_r.previous = M->previous;

    INTEGER_TYPE counter = 1;
    for (size_t i =1;i < A_r.y+1;) {
        double r = gsl_ran_flat(R, 0.01, 0.99);
        int k = ((log(r)/c) - 1.0);

        i += k + 1;
        if(i < A_r.y+1){
            elements[counter].kind = 'L';
            elements[counter].x = i;
            elements[counter].previous = &elements[counter-1];
            counter+=1;
        }
    }
    M->previous = &elements[counter-1] ;
    M->x = A_r.y +1;

    if(A_r.y != A_r.x){
        w wrapper;
        wrapper.m = &A_r;
        if((A_r.y)-(A_r.x) > (LIMIT) ){
            pthread_t thread;
            wrapper.r = gsl_rng_alloc (gsl_rng_taus);
            gsl_rng_set(wrapper.r,SEED+A_r.y);
            pthread_create( &thread, NULL, rule, &wrapper);
            if(M->x != M->y)
                rule(p);
            pthread_join(thread,NULL);
            gsl_rng_free(wrapper.r);
        } else {
        wrapper.r = R;
        rule(&wrapper);
        if(M->x != M->y)
            rule(p);
    } }else{
        if(M->x != M->y)
          rule(p);
    }
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
                /* printf("\n"); */
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
        /* printf("%c(%d,%d)",chain-> kind,chain->x,chain->y); */
        chain = chain->previous;
    }while (chain != NULL);
    /* fprintf(fptr, "}\n }"); */
    fclose(fptr);
    return 0;
}


int main(int argc, char *argv[]) {
    sscanf(argv[1],"%d", &MAX);
    sscanf(argv[2], "%lf", &P);

    c = log(1.0-P);

    pre_alloc = malloc(MAX*MAX*sizeof(module));
    INTEGER_TYPE max = MAX;
    module* iv = (module*)malloc(sizeof(module));
    iv->kind = 'A';
    iv->x = 1;
    iv->y = max;

    gsl_rng *rand_src;
    rand_src = gsl_rng_alloc (gsl_rng_taus);

    w wrapper;
    wrapper.m = iv;
    wrapper.r = rand_src;
    gsl_rng_set(wrapper.r,SEED);
    struct timespec start={0,0}, end={0,0};
    clock_gettime(CLOCK_MONOTONIC, &start);
    rule(&wrapper);
    clock_gettime(CLOCK_MONOTONIC, &end);
    gsl_rng_free(rand_src);
    /* write_file(iv); */
    printf("%.10fs\n",((end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec)));
    /* printf("c=%lf \n",c); */
    free(pre_alloc);
    free(iv);
}
