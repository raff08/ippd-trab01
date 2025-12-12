# Reprodutibilidade dos Experimentos

Este documento contém todas as informações necessárias para reproduzir os experimentos realizados neste trabalho.

## Resumo Executivo - Configuração do Sistema

| Componente | Especificação |
|------------|---------------|
| **CPU** | AMD Ryzen 5 7535HS (6 cores, 12 threads) |
| **Arquitetura** | x86_64, Zen 3+ |
| **SIMD** | AVX, AVX2, FMA, SSE4.1, SSE4.2 |
| **SO** | Ubuntu 24.04.2 LTS (WSL2) |
| **Kernel** | Linux 5.15.146.1-microsoft-standard-WSL2 |
| **Compilador** | GCC 13.3.0 |
| **OpenMP** | 4.5 (201511) |
| **Python** | 3.12.3 |
| **Pandas** | 2.1.4 |
| **Matplotlib** | 3.6.3 |
| **NumPy** | 1.26.4 |

**Nota:** Experimentos executados em WSL2, o que limita controle sobre frequency scaling e pode introduzir variância adicional.

## Informações do Sistema

### Sistema Operacional
```
Linux Rafael 5.15.146.1-microsoft-standard-WSL2 #1 SMP Thu Jan 11 04:09:03 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

Ubuntu 24.04.2 LTS (Noble Numbat)
```

**Ambiente:** WSL2 (Windows Subsystem for Linux 2)
**Distribuição:** Ubuntu 24.04.2 LTS
**Kernel:** Linux 5.15.146.1-microsoft-standard-WSL2

### Processador (CPU)

```
Architecture:                       x86_64
Model name:                         AMD Ryzen 5 7535HS with Radeon Graphics
CPU(s):                             12
Thread(s) per core:                 2
Core(s) per socket:                 6
Socket(s):                          1
```

**Informações relevantes:**
- **Modelo da CPU:** AMD Ryzen 5 7535HS with Radeon Graphics
- **Arquitetura:** x86_64
- **Número de cores físicos:** 6
- **Número de threads (hyperthreading):** 12 (2 threads por core)
- **Sockets:** 1
- **Suporte SIMD:** AVX, AVX2, FMA, SSE4.1, SSE4.2, AES
  - Flags relevantes detectadas: `avx avx2 fma sse4_1 sse4_2 aes f16c`
- **Características:** Zen 3+ architecture (Rembrandt)

### Compilador

**GCC:**
```
gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Copyright (C) 2023 Free Software Foundation, Inc.
```

**Versão do OpenMP:**
```
OpenMP 4.5 (201511)
#define _OPENMP 201511
```

**Nota:** OpenMP 4.5 suporta as principais features utilizadas neste trabalho:
- `#pragma omp simd`
- `#pragma omp parallel for simd`
- Todas as cláusulas de schedule utilizadas

### Python e Bibliotecas

```
Python 3.12.3

Bibliotecas utilizadas:
- matplotlib 3.6.3
- numpy 1.26.4
- pandas 2.1.4+dfsg
```

## Flags de Compilação

### Sequencial
```makefile
CFLAGS = -O3 -Wall -march=native
LDFLAGS = -lm
```

### Paralelo (OpenMP)
```makefile
CFLAGS = -O3 -Wall -march=native -fopenmp
LDFLAGS = -lm -fopenmp
```

### Explicação das Flags

- **`-O3`**: Nível máximo de otimização do GCC
  - Ativa otimizações agressivas (loop unrolling, function inlining, etc.)
  - Pode aumentar tamanho do binário mas melhora desempenho

- **`-Wall`**: Ativa todos os warnings principais
  - Ajuda a identificar potenciais problemas no código

- **`-march=native`**: Otimiza para a arquitetura da CPU local
  - Habilita instruções SIMD disponíveis (AVX, AVX2, etc.)

- **`-fopenmp`**: Ativa suporte a OpenMP
  - Necessário para compilar diretivas `#pragma omp`

- **`-lm`**: Linka biblioteca matemática
  - Necessário para `sqrt()`, `sqrtf()`, etc.

---

## Configurações de Execução

### Afinidade de CPU (CPU Affinity)

**Variáveis de ambiente OpenMP:**

**Configuração utilizada nos experimentos:**
```bash
OMP_PROC_BIND=not_set (padrão do sistema)
OMP_PLACES=not_set (padrão do sistema)
OMP_DYNAMIC=not_set (padrão do sistema)
```

**Nota importante:**
- Os programas configuram explicitamente `omp_set_num_threads()` no código
- Variáveis de ambiente OpenMP não foram definidas (valores padrão)
- Isso permite reprodução consistente independente do ambiente do usuário
- Para experimentos ainda mais controlados, pode-se definir:
  ```bash
  export OMP_PROC_BIND=close
  export OMP_PLACES=cores
  export OMP_DYNAMIC=false
  ```

### Frequência da CPU (CPU Scaling)

**Status:** N/A (WSL2)

```
CPU Frequency Scaling: Não disponível no WSL2
```

**Nota importante sobre WSL2:**
- WSL2 não expõe controle de CPU frequency scaling
- A frequência é gerenciada pelo Windows host
- Possível variação de frequência durante execução (impacto na variância)"

---

## Semente do Gerador de Números Aleatórios

Todos os programas utilizam **semente fixa** para garantir reprodutibilidade:

```c
srand(42);  // Semente fixa em todos os programas
```

Esta semente garante que:
- Os vetores de entrada sejam idênticos entre execuções
- Resultados possam ser comparados de forma justa
- Experimentos sejam reproduzíveis

---

## Parâmetros dos Experimentos

### Tamanhos de Entrada (N)
- 100.000
- 500.000
- 1.000.000

### Número de Threads
- 1, 2, 4, 8, 16

### Repetições
- 5 execuções por configuração
- Cálculo de média e desvio padrão

---

## Procedimento de Medição

### Função de Medição de Tempo

```c
double get_wall_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}
```

**Características:**
- Usa `CLOCK_MONOTONIC` para evitar ajustes de relógio do sistema
- Precisão de nanossegundos
- Mede tempo de parede (wall-clock time)

### Região Medida

Para todas as tarefas:
```c
double start = get_wall_time();
// Kernel sendo medido
double end = get_wall_time();
double elapsed = end - start;
```

**O que é medido:**
- Apenas o kernel de computação
- **NÃO** inclui: alocação de memória, inicialização, I/O

---

### Verificação de Estabilidade

O desvio padrão das 5 repetições indica estabilidade:
- **Baixo desvio (< 5% da média):** Medições estáveis ✓
- **Alto desvio (> 10% da média):** Investigar causa de variabilidade ✗


