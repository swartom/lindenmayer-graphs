#include "hyper_cube.h"
#include <pthread.h>
#include <time.h>

typedef struct parametric_module {
    void * previous;
    uint8_t kind;
    INTEGER_TYPE x;
    INTEGER_TYPE y;
    uint8_t z;
} module;


int write_file(module* iv) {
    module* chain = iv;
    FILE *fptr;
    fptr = fopen("graph.adjlist", "w");
    /* fprintf(fptr, "graph {\nnode[shape=point]"); */
    int test = 0;
    do {
        /* printf("%c(%d,%d,%d)\n",chain->kind,chain->x,chain->y,chain->z); */
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
#define g(ARG1,ARG2) pow(2,ARG1) + ARG2
void* rule( void* p) {
    module*m = (module *) p;


    switch (m->kind) {
        case 'A': {
            module* elements = (module *) malloc(2*sizeof(module));
            #define A_x elements[0]
            #define L_g elements[1]


            A_x.kind = 'A';
            A_x.x = m->x;
            A_x.y = m->y + 1;
            A_x.z = 1;

            L_g.kind = 'L';
            L_g.y = m->x;
            L_g.x = g(m->y,m->x);
            L_g.z = (uint8_t) m->y + 1;


            m->x = L_g.x;
            m->y = m->y + 1;
            m->z = 1;

            L_g.previous = m->previous;
            A_x.previous = &L_g;
            m->previous = &A_x;

            if (A_x.y < ORDER) {
                if (A_x.y <= THREADS) {
                pthread_t thread1,thread2;
                pthread_create( &thread1, NULL, rule, &A_x);
                pthread_create( &thread2, NULL, rule, &L_g);
                rule(m);
                pthread_join(thread1,NULL);
                pthread_join(thread2,NULL);
                } else {
                    rule(&A_x);
                    rule(&L_g);
                    rule(m);
                }
            }
            break;}
        case 'L':{
            module* elements = (module *) malloc(3*sizeof(module));

            #define j m->z

            #define L_gx elements[0]
            #define A_y elements[1]
            #define L_x elements[2]

            L_gx.kind = 'L';
            L_gx.x = g(j,m->x);
            L_gx.y = g(j,m->y);
            L_gx.z = j + 1;

            A_y.kind = 'A';
            A_y.x = m->y;

            L_x.kind = 'L';
            L_x.x = m->x ; //g(j,m->x);
            L_x.y = m->y; // m->x;
            L_x.z = j + 1;

            m->kind = 'A';
            m->x = g(j,m->y);

            L_x.previous = m->previous;
            A_y.previous = &L_x;
            L_gx.previous = &A_y;
            m->previous = &L_gx;

            if (L_x.z < ORDER) {
                pthread_t thread1;
                if (L_x.z <= THREADS){
                pthread_create( &thread1, NULL, rule, &L_x);
                rule(&L_gx);
                pthread_join(thread1,NULL);
                    } else {
                        rule(&L_gx);
                        rule(&L_x);
                    }


            }
            break;
        }
    }
    return 0;
}
int write_dot_file(module* iv) {
    module* chain = iv;
    FILE *fptr;
    fptr = fopen("graph.dot", "w");
    fprintf(fptr, "graph {overlap=prism\ndimen=3\nrepulsiveforce=1\n\nbeautify=true \n \nnode[shape=point,width=.001,color=\"maroon\"]\nedge[penwidth=0.01,color=\"gray\"]");
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

    module* iv = (module*)malloc(sizeof(module));
    iv->kind = 'A';
    iv->x = 1;
    iv->y = 0;

    struct timespec start={0,0}, end={0,0};
    clock_gettime(CLOCK_MONOTONIC, &start);
    rule(iv);
    clock_gettime(CLOCK_MONOTONIC, &end);
    printf("%.10fs\n",((end.tv_sec + 1.0e-9*end.tv_nsec) - (start.tv_sec + 1.0e-9*start.tv_nsec)));
    write_dot_file(iv);
    module* previous = iv;



    return 0;
}
