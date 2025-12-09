#include "sty_butadiene.h"

#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>


int MAX = 0;
int THREADS = 0;

#define INTEGER_TYPE uint32_t

typedef struct parametric_module {
    void * previous;
    uint8_t kind;
    INTEGER_TYPE x;
    INTEGER_TYPE y;
    INTEGER_TYPE z;

} module;

#define STYRENE  1
#define BUTADINE 2
#define STYRENE_INNER_DOUBLE_BOND 3
#define STYRENE_INNER_SINGLE_BOND 4
#define BUTADINE_INNER  1

static inline void new_module(module* addr,uint8_t kind, INTEGER_TYPE x, INTEGER_TYPE y, INTEGER_TYPE z ) {
    addr->kind = kind;
    addr->x = x;
    addr->y = y;
    addr->z = z;
}

void  rule(module* m ) {
    if(m->z == STYRENE) {
        module* elements = malloc(sizeof(module)*1);
        new_module(&elements[0], 'L',m->y,0,0);
        new_module(m, 'A',m->x,m->y,STYRENE_INNER_DOUBLE_BOND);
        elements[0].previous = m->previous;
        m->previous = &elements[0];
        rule(m);
    }
     else if (m->z == STYRENE_INNER_DOUBLE_BOND && m->x != m->y) {
        module* elements = malloc(sizeof(module)*3);
        new_module(&elements[0], 'A',m->x,0,0);
        new_module(&elements[1], 'L',m->x,0,0);
        new_module(&elements[2], 'L',m->x,0,0);
        new_module(m, 'A',m->x+1,m->y,STYRENE_INNER_SINGLE_BOND);
        elements[0].previous = m->previous;
        elements[1].previous = &elements[0];
        elements[2].previous = &elements[1];
        m->previous = &elements[2];
        rule(m);
    }else if (m->z == STYRENE_INNER_SINGLE_BOND && m->x != m->y) {
        module* elements = malloc(sizeof(module)*2);
        new_module(&elements[0], 'A',m->x,0,0);
        new_module(&elements[1], 'L',m->x,0,0);
        new_module(m, 'A',m->x+1,m->y,STYRENE_INNER_DOUBLE_BOND);
        elements[0].previous = m->previous;
        elements[1].previous = &elements[0];
        m->previous = &elements[1];
        rule(m);
    }
    else if(m-> z == BUTADINE && m->x != m->y) {
        module* elements = malloc(sizeof(module)*2);
        new_module(&elements[0], 'A',m->x,0,0);
        new_module(&elements[1], 'L',m->x,0,0);
        new_module(m, 'A',m->x+1,m->y,BUTADINE);
        elements[0].previous = m->previous;
        elements[1].previous = &elements[0];
        m->previous = &elements[1];
        rule(m);
    }
    else if (m-> z == 0){
        module* elements = malloc(sizeof(module)*20);

        int x = m->x;

        for (int i =1; i < 20; i++ )
            elements[i].previous = &elements[i-1];

        new_module(&elements[0] ,'A',x,x+5,STYRENE);
        new_module(&elements[1] ,'L',x,0,0);
        new_module(&elements[2] ,'A',x+6,x+9,BUTADINE);
        new_module(&elements[3] ,'L',x+9,0,0);
        new_module(&elements[4] ,'L',x+9,0,0);
        new_module(&elements[5] ,'A',x+10,x+13,BUTADINE);
        new_module(&elements[6] ,'L',x+14,0,0);
        new_module(&elements[7] ,'A',x+12,0,0);
        new_module(&elements[8] ,'A',x+14,x+19,STYRENE);
        new_module(&elements[9] ,'L',x+13,0,0);
        new_module(&elements[10],'A',x+20,x+23,BUTADINE);
        new_module(&elements[11],'L',x+22,0,0);
        new_module(&elements[12],'A',x+23,0,0);
        new_module(&elements[13],'L',x+21,0,0);
        new_module(&elements[14],'A',x+24,x+27,BUTADINE);
        new_module(&elements[15],'L',x+24,0,0);
        new_module(&elements[16],'A',x+28,x+33,STYRENE);
        new_module(&elements[17],'L',x+26,0,0);
        new_module(&elements[18],'A',x+34,x+39,STYRENE);

        new_module(&elements[19],'L',x+27,0,0);
        new_module(m,'A',x+40,m->y,0);
        elements[0].previous = m->previous;
        m->previous = &elements[19];


        if  (m->z == 0 && m->x + 39 <= m->y) {
            rule(m);
        }
        else {
            m->previous = &elements[18];
            m->x = 1;
        }
        int data[8] = {0,2,5,8,10,14,16,18};

        for (int i = 0; i < 8; i ++) {
            rule(&elements[data[i]]);
        }
    }

}


int write_file(module* iv) {
    module* chain = iv;
    FILE *fptr;
    fptr = fopen("graph.adjlist", "w");
    /* fprintf(fptr, "graph {\nnode[shape=point]"); */
    int test = 0;
    do {
        printf("%c(%d,%d,%d)",chain->kind,chain->x,chain->y,chain->z);
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
    fptr = fopen("graph_.dot", "w");
    fprintf(fptr, "graph {overlap=prism\ndimen=3\nrepulsiveforce=1\n\nbeautify=true \n \nnode[shape=point,width=.001,color=\"maroon\"]\nedge[penwidth=0.1,color=\"black\"]");
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

    module* iv = (module*)malloc(sizeof(module));
    iv->kind = 'A';
    iv->x = 1;
    iv->y = MAX * 40;

    rule(iv);
    write_file(iv);
}
