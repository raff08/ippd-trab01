#!/bin/bash

set -e

OUTPUT_FILE="results.csv"

N_VALUES=(100000 500000 1000000)
K_VALUES=(20 24 28)
THREADS=(1 2 4 8 16)
CHUNKS=(1 4 16 64)
REPETITIONS=5

echo "Compilando programas..."
make clean
make all

echo "Iniciando experimentos..."
echo "tarefa,n,k,threads,chunk,tempo" > "$OUTPUT_FILE"

echo "=== Tarefa A - Laço Irregular e Políticas de Schedule ==="

for n in "${N_VALUES[@]}"; do
    for k in "${K_VALUES[@]}"; do
        echo "  N=$n, K=$k"

        echo "    Sequencial..."
        for rep in $(seq 1 $REPETITIONS); do
            ./bin/tarefa_a_seq $n $k >> "$OUTPUT_FILE"
        done

        for t in "${THREADS[@]}"; do
            echo "    Static (threads=$t)..."
            for rep in $(seq 1 $REPETITIONS); do
                ./bin/tarefa_a_static $n $k $t >> "$OUTPUT_FILE"
            done

            for chunk in "${CHUNKS[@]}"; do
                echo "    Dynamic (threads=$t, chunk=$chunk)..."
                for rep in $(seq 1 $REPETITIONS); do
                    ./bin/tarefa_a_dynamic $n $k $t $chunk >> "$OUTPUT_FILE"
                done

                echo "    Guided (threads=$t, chunk=$chunk)..."
                for rep in $(seq 1 $REPETITIONS); do
                    ./bin/tarefa_a_guided $n $k $t $chunk >> "$OUTPUT_FILE"
                done
            done
        done
    done
done

echo "=== Tarefa C - SAXPY ==="

for n in "${N_VALUES[@]}"; do
    echo "  N=$n"

    echo "    Sequencial..."
    for rep in $(seq 1 $REPETITIONS); do
        ./bin/tarefa_c_seq $n | awk -F',' '{print $1","$2",NA,"$3",NA,"$4}' >> "$OUTPUT_FILE"
    done

    echo "    SIMD..."
    for rep in $(seq 1 $REPETITIONS); do
        ./bin/tarefa_c_simd $n | awk -F',' '{print $1","$2",NA,"$3",NA,"$4}' >> "$OUTPUT_FILE"
    done

    for t in "${THREADS[@]}"; do
        echo "    Parallel+SIMD (threads=$t)..."
        for rep in $(seq 1 $REPETITIONS); do
            ./bin/tarefa_c_parallel_simd $n $t | awk -F',' '{print $1","$2",NA,"$3",NA,"$4}' >> "$OUTPUT_FILE"
        done
    done
done

echo "=== Tarefa D - Organização de Região Paralela ==="

for n in "${N_VALUES[@]}"; do
    echo "  N=$n"

    for t in "${THREADS[@]}"; do
        echo "    Ingênua (threads=$t)..."
        for rep in $(seq 1 $REPETITIONS); do
            ./bin/tarefa_d_ingenua $n $t | awk -F',' '{print $1","$2",NA,"$3",NA,"$4}' >> "$OUTPUT_FILE"
        done

        echo "    Otimizada (threads=$t)..."
        for rep in $(seq 1 $REPETITIONS); do
            ./bin/tarefa_d_otimizada $n $t | awk -F',' '{print $1","$2",NA,"$3",NA,"$4}' >> "$OUTPUT_FILE"
        done
    done
done

echo "Experimentos concluídos. Resultados salvos em $OUTPUT_FILE"
