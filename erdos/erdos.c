#include "erdos.h"


int MAX = 0;
double P = 0.01;

#define LIMIT (MAX/((1.5)*THREADS))
#define THREADS 32


double c = 0;
module * restrict pre_alloc;
double get_random() { return (double)rand() / (double)RAND_MAX; }
void* rule( void* p) {
    module * m = (module*)p;
    uint32_t mid  = 3*((m->y) - (m->x))/4 + m->x; // r-1

    module* elements = (module*) &pre_alloc[(mid)*(MAX)];

    #define A_r elements[0]

    A_r.kind = 'A';
    A_r.x = m->x;
    A_r.y = mid;
    A_r.previous = m->previous;

    INTEGER_TYPE counter = 1;
    for (size_t i =1;i < A_r.y+1;) {
        double r = get_random();
        int k = ((log(r)/c) - 1.0);

        i += k + 1;
        if(i < A_r.y+1){
            elements[counter].kind = 'L';
            elements[counter].x = i;
            elements[counter].previous = &elements[counter-1];
            counter+=1;
        }
    }
    m->previous = &elements[counter-1] ;
    m->x = A_r.y +1;

    if(A_r.y != A_r.x){
        if((A_r.y)-(A_r.x) > (LIMIT) ){
            pthread_t thread;
            pthread_create( &thread, NULL, rule, &A_r);
            if(m->x != m->y)
                rule(m);
            pthread_join(thread,NULL);

        } else {
        rule(&A_r);
        if(m->x != m->y)
            rule(m);
    } }else{
        if(m->x != m->y)
          rule(m);
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


    struct timespec start={0,0}, end={0,0};


    clock_gettime(CLOCK_MONOTONIC, &start);
    rule(iv);
    clock_gettime(CLOCK_MONOTONIC, &end);

    /* write_file(iv); */
    printf("%.10fms\n",((end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec))*1000);
    printf("c=%lf \n",c);
    free(pre_alloc);
    free(iv);
}
