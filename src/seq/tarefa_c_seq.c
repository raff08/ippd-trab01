#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

double get_wall_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

void saxpy_seq(int n, float a, float *x, float *y) {
    for (int i = 0; i < n; i++) {
        y[i] = a * x[i] + y[i];
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Uso: %s <N>\n", argv[0]);
        fprintf(stderr, "Exemplo: %s 1000000\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    if (n <= 0) {
        fprintf(stderr, "Erro: N deve ser positivo\n");
        return 1;
    }

    float a = 2.5f;
    float *x = (float *)malloc(n * sizeof(float));
    float *y = (float *)malloc(n * sizeof(float));

    if (!x || !y) {
        fprintf(stderr, "Erro ao alocar memória\n");
        free(x);
        free(y);
        return 1;
    }

    srand(42);
    for (int i = 0; i < n; i++) {
        x[i] = (float)rand() / RAND_MAX;
        y[i] = (float)rand() / RAND_MAX;
    }

    double start = get_wall_time();
    saxpy_seq(n, a, x, y);
    double end = get_wall_time();

    double elapsed = end - start;

    printf("tarefa_c_seq,%d,1,%.6f\n", n, elapsed);

    free(x);
    free(y);

    return 0;
}
