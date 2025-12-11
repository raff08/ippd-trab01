#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <math.h>

double get_wall_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

void process_otimizada(int n, float *a, float *b, float *c, float *d) {
    #pragma omp parallel
    {
        #pragma omp for
        for (int i = 0; i < n; i++) {
            c[i] = sqrtf(a[i] * a[i] + b[i] * b[i]);
        }

        #pragma omp for
        for (int i = 0; i < n; i++) {
            d[i] = c[i] * 2.0f + a[i];
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Uso: %s <N> <threads>\n", argv[0]);
        fprintf(stderr, "Exemplo: %s 1000000 4\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    int threads = atoi(argv[2]);

    if (n <= 0 || threads <= 0) {
        fprintf(stderr, "Erro: N e threads devem ser positivos\n");
        return 1;
    }

    omp_set_num_threads(threads);

    float *a = (float *)malloc(n * sizeof(float));
    float *b = (float *)malloc(n * sizeof(float));
    float *c = (float *)malloc(n * sizeof(float));
    float *d = (float *)malloc(n * sizeof(float));

    if (!a || !b || !c || !d) {
        fprintf(stderr, "Erro ao alocar memória\n");
        free(a); free(b); free(c); free(d);
        return 1;
    }

    srand(42);
    for (int i = 0; i < n; i++) {
        a[i] = (float)rand() / RAND_MAX;
        b[i] = (float)rand() / RAND_MAX;
    }

    double start = get_wall_time();
    process_otimizada(n, a, b, c, d);
    double end = get_wall_time();

    double elapsed = end - start;

    printf("tarefa_d_otimizada,%d,%d,%.6f\n", n, threads, elapsed);

    free(a);
    free(b);
    free(c);
    free(d);

    return 0;
}
