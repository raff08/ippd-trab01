#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double get_wall_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

long long fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Uso: %s <N> <K>\n", argv[0]);
        fprintf(stderr, "Exemplo: %s 100000 20\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    int k = atoi(argv[2]);

    if (n <= 0 || k <= 0) {
        fprintf(stderr, "Erro: N e K devem ser positivos\n");
        return 1;
    }

    long long *v = (long long *)malloc(n * sizeof(long long));
    if (!v) {
        fprintf(stderr, "Erro ao alocar memória\n");
        return 1;
    }

    double start = get_wall_time();

    for (int i = 0; i < n; i++) {
        v[i] = fib(i % k);
    }

    double end = get_wall_time();
    double elapsed = end - start;

    printf("tarefa_a_seq,%d,%d,1,NA,%.6f\n", n, k, elapsed);

    free(v);
    return 0;
}
