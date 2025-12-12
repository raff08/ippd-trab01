# Trabalho OpenMP - Tarefas A, C e D

## Integrantes do Grupo
- Sofia Petersen - Responsável pela implementação da Tarefa A (Laço Irregular e Políticas de Schedule)
- Rafael Freitas - Responsável pela implementação da Tarefa C (Vetorização SIMD) e scripts de automação/documentação
- Pedro Ravazolo - Responsável pela implementação da Tarefa D (Organização de Região Paralela) e geração dos gráficos
- Todos participaram conjuntamente da análise e dos resultados finais, embora apenas um tenha feito o commit por uma questão de praticidade, já que realizamos a análise presencialmente.

## Tarefas Implementadas

### Tarefa A - Laço Irregular e Políticas de Schedule
Kernel Fibonacci recursivo sem memoização aplicado a um laço irregular: `v[i] = fib(i % K)`

**Variantes:**
- Sequencial ([tarefa_a_seq.c](src/seq/tarefa_a_seq.c))
- V1: `schedule(static)` ([tarefa_a_static.c](src/omp/tarefa_a_static.c))
- V2: `schedule(dynamic, chunk)` com chunk ∈ {1, 4, 16, 64} ([tarefa_a_dynamic.c](src/omp/tarefa_a_dynamic.c))
- V3: `schedule(guided, chunk)` com chunk ∈ {1, 4, 16, 64} ([tarefa_a_guided.c](src/omp/tarefa_a_guided.c))

**Parâmetros experimentais:**
- N ∈ {100.000, 500.000, 1.000.000}
- K ∈ {20, 24, 28} (grau de irregularidade)
- Threads ∈ {1, 2, 4, 8, 16}

### Tarefa C - Vetorização com SIMD (SAXPY)
Implementação do kernel SAXPY: `y[i] = a*x[i] + y[i]`

**Variantes:**
- V1: Sequencial ([tarefa_c_seq.c](src/seq/tarefa_c_seq.c))
- V2: `#pragma omp simd` ([tarefa_c_simd.c](src/omp/tarefa_c_simd.c))
- V3: `#pragma omp parallel for simd` ([tarefa_c_parallel_simd.c](src/omp/tarefa_c_parallel_simd.c))

### Tarefa D - Organização de Região Paralela
Comparação de overhead entre diferentes organizações de regiões paralelas.

**Variantes:**
- Ingênua: Dois `#pragma omp parallel for` consecutivos ([tarefa_d_ingenua.c](src/omp/tarefa_d_ingenua.c))
- Otimizada: Uma região `#pragma omp parallel` com dois `for` internos ([tarefa_d_otimizada.c](src/omp/tarefa_d_otimizada.c))

## Estrutura do Projeto

```
trabalho_openMP/
├── src/
│   ├── seq/              # Implementações sequenciais
│   │   ├── tarefa_a_seq.c
│   │   └── tarefa_c_seq.c
│   └── omp/              # Implementações paralelas com OpenMP
│       ├── tarefa_a_static.c
│       ├── tarefa_a_dynamic.c
│       ├── tarefa_a_guided.c
│       ├── tarefa_c_simd.c
│       ├── tarefa_c_parallel_simd.c
│       ├── tarefa_d_ingenua.c
│       └── tarefa_d_otimizada.c
├── bin/                  # Binários compilados (gerado automaticamente)
├── Makefile              # Sistema de compilação
├── run.sh                # Script de execução dos experimentos
├── plot.py               # Script de geração de gráficos
├── README.md             # Este arquivo
├── RESULTADOS.md         # Análise de resultados 
└── REPRODUCIBILIDADE.md  # Informações de reprodutibilidade
```

## Pré-requisitos

- GCC com suporte a OpenMP 5.x
- Python 3 com pandas e matplotlib
- Sistema operacional Linux

```bash
# Ubuntu/Debian
sudo apt install build-essential python3 python3-pip
pip3 install pandas matplotlib numpy
```

## Como Compilar

### Compilar tudo (sequencial + paralelo)
```bash
make
```

### Compilar apenas versões sequenciais
```bash
make seq
```

### Compilar apenas versões paralelas
```bash
make omp
```

### Limpar arquivos gerados
```bash
make clean
```

## Como Executar

### Execução manual de um programa específico

**Tarefa C - Sequencial:**
```bash
./bin/tarefa_c_seq <N>
```
Exemplo:
```bash
./bin/tarefa_c_seq 1000000
```

**Tarefa C - SIMD:**
```bash
./bin/tarefa_c_simd <N>
```

**Tarefa C - Parallel + SIMD:**
```bash
./bin/tarefa_c_parallel_simd <N> <threads>
```
Exemplo:
```bash
./bin/tarefa_c_parallel_simd 1000000 4
```

**Tarefa D - Ingênua:**
```bash
./bin/tarefa_d_ingenua <N> <threads>
```

**Tarefa D - Otimizada:**
```bash
./bin/tarefa_d_otimizada <N> <threads>
```

### Execução automática de todos os experimentos

```bash
make run
```

ou

```bash
./run.sh
```

Este comando:
1. Compila todos os programas
2. Executa a matriz completa de experimentos
3. Gera o arquivo `results.csv` com todos os resultados

**Parâmetros dos experimentos:**
- **Tarefa A:** N ∈ {100000, 500000, 1000000}, K ∈ {20, 24, 28}, Threads ∈ {1, 2, 4, 8, 16}, Chunks ∈ {1, 4, 16, 64}
- **Tarefas C e D:** N ∈ {100000, 500000, 1000000}, Threads ∈ {1, 2, 4, 8, 16}
- Cada configuração: 5 repetições para cálculo de média e desvio padrão

## Como Gerar Gráficos

Após executar os experimentos:

```bash
make plot
```

ou

```bash
python3 plot.py
```

**Gráficos gerados:**

1. `tarefa_a_schedule_comparison.png` - Comparação detalhada de políticas de schedule para Tarefa A
2. `tarefa_a_speedup.png` - Speedup das melhores configurações de schedule
3. `tarefa_c_tempo.png` - Tempo de execução da Tarefa C para diferentes tamanhos de N
4. `tarefa_c_speedup.png` - Speedup da Tarefa C em relação à versão sequencial
5. `tarefa_d_tempo.png` - Comparação de tempo entre versões ingênua e otimizada
6. `tarefa_d_overhead.png` - Overhead percentual da versão ingênua sobre a otimizada
7. `summary.txt` - Tabela com estatísticas (média e desvio padrão)

## Análise de Resultados

Os resultados detalhados e análises estão no arquivo [RESULTADOS.md](RESULTADOS.md).

## Informações de Reprodutibilidade

Consulte [REPRODUCIBILIDADE.md](REPRODUCIBILIDADE.md) para informações sobre:
- Versão do compilador e flags de compilação
- Especificações da CPU
- Configurações de afinidade
- Semente do gerador de números aleatórios

## Decisões de Implementação

### Tarefa A - Laço Irregular

**Escolha do kernel Fibonacci:**
- Fibonacci recursivo sem memoização cria carga computacional heterogênea
- `fib(i % K)` gera desbalanceamento: iterações com valores menores terminam mais rápido
- Permite avaliar efetivamente diferentes políticas de escalonamento

**Políticas de schedule testadas:**
1. **Static:** Divide trabalho igualmente no início - ruim para cargas desbalanceadas
2. **Dynamic:** Distribui blocos de tamanho `chunk` dinamicamente - boa adaptação mas overhead de sincronização
3. **Guided:** Blocos começam grandes e diminuem exponencialmente - compromisso entre balanceamento e overhead

**Valores de K testados:**
- K=20: Moderadamente irregular (fib(0) a fib(19))
- K=24: Mais irregular
- K=28: Máxima irregularidade testada (fib(27) é muito custoso)

### Tarefa C - SAXPY

**Escolha de SIMD:**
- O kernel SAXPY é ideal para vetorização SIMD pois:
  - Operações aritméticas simples (multiplicação e adição)
  - Acesso sequencial à memória
  - Sem dependências entre iterações
  - Tipo de dado `float` permite empacotamento eficiente em registradores SIMD

**Combinação `parallel for simd`:**
- Combina paralelismo em nível de thread (parallel for) com vetorização (simd)
- Threads dividem o trabalho e cada thread usa instruções SIMD
- Melhor escalabilidade para vetores grandes

### Tarefa D - Organização de Região Paralela

**Problema com versão ingênua:**
- Dois `#pragma omp parallel for` consecutivos criam e destroem a equipe de threads duas vezes
- Overhead de sincronização e criação/destruição de threads

**Solução otimizada:**
- Uma única região `#pragma omp parallel` com dois `#pragma omp for`
- Threads são criadas uma única vez
- Barreira implícita entre os dois laços garante sincronização
- Reduz significativamente o overhead

## Observações

- Todos os programas usam semente fixa (42) para garantir reprodutibilidade
- Medição de tempo usa `clock_gettime(CLOCK_MONOTONIC)` para precisão
- Flags de compilação: `-O3 -march=native` para otimização máxima
- Saída em formato CSV para facilitar análise automatizada
