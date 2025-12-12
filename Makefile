CC = gcc
CFLAGS = -O3 -Wall -march=native
LDFLAGS = -lm

SEQ_DIR = src/seq
OMP_DIR = src/omp
BIN_DIR = bin

SEQ_SOURCES = $(wildcard $(SEQ_DIR)/*.c)
OMP_SOURCES = $(wildcard $(OMP_DIR)/*.c)

SEQ_BINS = $(patsubst $(SEQ_DIR)/%.c,$(BIN_DIR)/%,$(SEQ_SOURCES))
OMP_BINS = $(patsubst $(OMP_DIR)/%.c,$(BIN_DIR)/%,$(OMP_SOURCES))

.PHONY: all seq omp clean run plot

all: seq omp

seq: $(SEQ_BINS)

omp: $(OMP_BINS)

$(BIN_DIR)/%: $(SEQ_DIR)/%.c | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

$(BIN_DIR)/%: $(OMP_DIR)/%.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -fopenmp $< -o $@ $(LDFLAGS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

clean:
	rm -rf $(BIN_DIR) results.csv *.png

run:
	./run.sh

plot:
	python3 plot.py
