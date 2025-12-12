# Guia Rápido 

## Instalação de Dependências

```bash
# Ubuntu/Debian
sudo apt install build-essential python3 python3-pip
pip3 install pandas matplotlib numpy
```

## Compilar e Executar - 3 Passos

### 1. Compilar
```bash
make
```

### 2. Executar Experimentos
```bash
./run.sh
```
Isso vai gerar o arquivo `results.csv` com todos os dados.

### 3. Gerar Gráficos
```bash
python3 plot.py
```

Gráficos gerados:
- `tarefa_a_schedule_comparison.png` - Comparação de schedule policies (static, dynamic, guided)
- `tarefa_a_speedup.png` - Speedup das melhores configurações
- `tarefa_c_tempo.png` - Tempo de execução SAXPY
- `tarefa_c_speedup.png` - Speedup SAXPY
- `tarefa_d_tempo.png` - Comparação ingênua vs otimizada
- `tarefa_d_overhead.png` - Overhead da versão ingênua
- `summary.txt` - Estatísticas em texto

## Visualizar Resultados

```bash
cat summary.txt
```

## Limpar

```bash
make clean
```

## Estrutura dos Arquivos

```
trabalho_openMP/
├── src/
│   ├── seq/
│   │   ├── tarefa_a_seq.c           # Fibonacci sequencial
│   │   └── tarefa_c_seq.c           # SAXPY sequencial
│   └── omp/
│       ├── tarefa_a_static.c        # Schedule static
│       ├── tarefa_a_dynamic.c       # Schedule dynamic
│       ├── tarefa_a_guided.c        # Schedule guided
│       ├── tarefa_c_simd.c          # SAXPY com SIMD
│       ├── tarefa_c_parallel_simd.c # SAXPY paralelo + SIMD
│       ├── tarefa_d_ingenua.c       # 2x parallel for
│       └── tarefa_d_otimizada.c     # 1x parallel region
├── Makefile                          # Build system
├── run.sh                            # Executa experimentos
├── plot.py                           # Gera gráficos
├── README.md                         # Documentação completa
├── RESULTADOS.md                     # Análise de resultados
└── REPRODUCIBILIDADE.md              # Info de reprodutibilidade
```

## Testes Manuais

### Tarefa A - Schedule Policies
```bash
# Sequencial
./bin/tarefa_a_seq 1000000 28

# Static
./bin/tarefa_a_static 1000000 28 4

# Dynamic (chunk=4)
./bin/tarefa_a_dynamic 1000000 28 4 4

# Guided (chunk=4)
./bin/tarefa_a_guided 1000000 28 4 4
```

### Tarefa C - SAXPY
```bash
./bin/tarefa_c_seq 1000000
./bin/tarefa_c_simd 1000000
./bin/tarefa_c_parallel_simd 1000000 4
```

### Tarefa D - Região Paralela
```bash
./bin/tarefa_d_ingenua 1000000 4
./bin/tarefa_d_otimizada 1000000 4
```

