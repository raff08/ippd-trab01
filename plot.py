#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def load_data(filename='results.csv'):
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"Erro: arquivo {filename} não encontrado.")
        print("Execute './run.sh' primeiro para gerar os resultados.")
        sys.exit(1)

def calculate_stats(df):
    # Para Tarefa A - separar seq/static (sem chunk) de dynamic/guided (com chunk)
    df_a = df[df['tarefa'].str.contains('tarefa_a')].copy()

    # Seq e Static não têm chunk
    stats_a_no_chunk = df_a[df_a['tarefa'].isin(['tarefa_a_seq', 'tarefa_a_static'])].groupby(
        ['tarefa', 'n', 'k', 'threads'])['tempo'].agg(['mean', 'std']).reset_index()
    stats_a_no_chunk['chunk'] = np.nan

    # Dynamic e Guided têm chunk
    stats_a_with_chunk = df_a[df_a['tarefa'].isin(['tarefa_a_dynamic', 'tarefa_a_guided'])].groupby(
        ['tarefa', 'n', 'k', 'threads', 'chunk'])['tempo'].agg(['mean', 'std']).reset_index()

    # Combinar os dois
    stats_a = pd.concat([stats_a_no_chunk, stats_a_with_chunk], ignore_index=True)

    # Para Tarefa C e D (não tem k nem chunk)
    stats_cd = df[~df['tarefa'].str.contains('tarefa_a')].groupby(
        ['tarefa', 'n', 'threads'])['tempo'].agg(['mean', 'std']).reset_index()

    return stats_a, stats_cd

def plot_tarefa_a_schedule_comparison(stats_a):
    """Comparação de schedule policies para diferentes K e chunks"""
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))

    n_values = sorted(stats_a['n'].unique())
    k_values = sorted(stats_a['k'].unique())

    for n_idx, n in enumerate(n_values):
        for k_idx, k in enumerate(k_values):
            ax = axes[k_idx, n_idx]

            data = stats_a[(stats_a['n'] == n) & (stats_a['k'] == k)]

            # Sequencial baseline
            seq = data[data['tarefa'] == 'tarefa_a_seq']
            if not seq.empty:
                seq_time = seq['mean'].values[0]
                ax.axhline(y=seq_time, color='black', linestyle='--',
                          label='Sequencial', linewidth=2, alpha=0.7)

            # Static
            static = data[data['tarefa'] == 'tarefa_a_static']
            if not static.empty:
                threads = static['threads'].values
                times = static['mean'].values
                ax.plot(threads, times, marker='s', label='Static', linewidth=2)

            # Dynamic - pegar melhor chunk
            for chunk in [1, 4, 16, 64]:
                dynamic = data[(data['tarefa'] == 'tarefa_a_dynamic') & (data['chunk'] == chunk)]
                if not dynamic.empty:
                    threads = dynamic['threads'].values
                    times = dynamic['mean'].values
                    ax.plot(threads, times, marker='o', label=f'Dynamic(chunk={chunk})', linewidth=1.5, alpha=0.7)

            # Guided - pegar melhor chunk
            for chunk in [1, 4, 16, 64]:
                guided = data[(data['tarefa'] == 'tarefa_a_guided') & (data['chunk'] == chunk)]
                if not guided.empty:
                    threads = guided['threads'].values
                    times = guided['mean'].values
                    ax.plot(threads, times, marker='^', label=f'Guided(chunk={chunk})', linewidth=1.5, alpha=0.7)

            ax.set_xlabel('Threads')
            ax.set_ylabel('Tempo (s)')
            ax.set_title(f'N={n}, K={k}')
            ax.set_xscale('log', base=2)
            ax.set_yscale('log')
            ax.grid(True, alpha=0.3)
            if k_idx == 0 and n_idx == 0:
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    plt.tight_layout()
    plt.savefig('tarefa_a_schedule_comparison.png', dpi=150, bbox_inches='tight')
    print("Gráfico salvo: tarefa_a_schedule_comparison.png")
    plt.close()

def plot_tarefa_a_best_configs(stats_a):
    """Speedup com as melhores configurações de cada schedule"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    n_values = sorted(stats_a['n'].unique())

    for idx, n in enumerate(n_values):
        ax = axes[idx]

        data_n = stats_a[stats_a['n'] == n]

        # Pegar K=28 (mais irregular)
        data = data_n[data_n['k'] == 28]

        # Sequencial
        seq = data[data['tarefa'] == 'tarefa_a_seq']
        if not seq.empty:
            seq_time = seq['mean'].values[0]

            # Static
            static = data[data['tarefa'] == 'tarefa_a_static']
            if not static.empty:
                threads = static['threads'].values
                speedups = seq_time / static['mean'].values
                ax.plot(threads, speedups, marker='s', label='Static', linewidth=2)

            # Dynamic - melhor chunk por thread
            dynamic_best = []
            for t in sorted(data['threads'].unique()):
                if pd.notna(t):
                    dynamic_t = data[(data['tarefa'] == 'tarefa_a_dynamic') & (data['threads'] == t)]
                    if not dynamic_t.empty:
                        best_idx = dynamic_t['mean'].idxmin()
                        dynamic_best.append(dynamic_t.loc[best_idx])

            if dynamic_best:
                dynamic_df = pd.DataFrame(dynamic_best)
                threads = dynamic_df['threads'].values
                speedups = seq_time / dynamic_df['mean'].values
                ax.plot(threads, speedups, marker='o', label='Dynamic(best)', linewidth=2)

            # Guided - melhor chunk por thread
            guided_best = []
            for t in sorted(data['threads'].unique()):
                if pd.notna(t):
                    guided_t = data[(data['tarefa'] == 'tarefa_a_guided') & (data['threads'] == t)]
                    if not guided_t.empty:
                        best_idx = guided_t['mean'].idxmin()
                        guided_best.append(guided_t.loc[best_idx])

            if guided_best:
                guided_df = pd.DataFrame(guided_best)
                threads = guided_df['threads'].values
                speedups = seq_time / guided_df['mean'].values
                ax.plot(threads, speedups, marker='^', label='Guided(best)', linewidth=2)

            # Linear ideal
            max_threads = 16
            ax.plot([1, 2, 4, 8, 16], [1, 2, 4, 8, 16], 'k--', alpha=0.3, label='Linear')

        ax.set_xlabel('Threads')
        ax.set_ylabel('Speedup')
        ax.set_title(f'Tarefa A - Speedup (N={n}, K=28)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log', base=2)

    plt.tight_layout()
    plt.savefig('tarefa_a_speedup.png', dpi=150)
    print("Gráfico salvo: tarefa_a_speedup.png")
    plt.close()

def plot_tarefa_c(stats):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    n_values = sorted(stats['n'].unique())

    for idx, n in enumerate(n_values):
        ax = axes[idx]

        data_n = stats[stats['n'] == n]

        seq = data_n[(data_n['tarefa'] == 'tarefa_c_seq')]
        simd = data_n[(data_n['tarefa'] == 'tarefa_c_simd')]
        parallel_simd = data_n[(data_n['tarefa'] == 'tarefa_c_parallel_simd')]

        if not seq.empty:
            seq_time = seq['mean'].values[0]
            ax.axhline(y=seq_time, color='gray', linestyle='--',
                      label='Sequencial', linewidth=2)

        if not simd.empty:
            simd_time = simd['mean'].values[0]
            ax.axhline(y=simd_time, color='orange', linestyle='--',
                      label='SIMD', linewidth=2)

        if not parallel_simd.empty:
            threads = parallel_simd['threads'].values
            times = parallel_simd['mean'].values
            stds = parallel_simd['std'].values

            ax.errorbar(threads, times, yerr=stds, marker='o',
                       capsize=5, label='Parallel+SIMD', linewidth=2)

        ax.set_xlabel('Threads')
        ax.set_ylabel('Tempo (s)')
        ax.set_title(f'Tarefa C - SAXPY (N={n})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log', base=2)

    plt.tight_layout()
    plt.savefig('tarefa_c_tempo.png', dpi=150)
    print("Gráfico salvo: tarefa_c_tempo.png")
    plt.close()

def plot_tarefa_c_speedup(stats):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    n_values = sorted(stats['n'].unique())

    for idx, n in enumerate(n_values):
        ax = axes[idx]

        data_n = stats[stats['n'] == n]

        seq = data_n[(data_n['tarefa'] == 'tarefa_c_seq')]
        simd = data_n[(data_n['tarefa'] == 'tarefa_c_simd')]
        parallel_simd = data_n[(data_n['tarefa'] == 'tarefa_c_parallel_simd')]

        if not seq.empty:
            seq_time = seq['mean'].values[0]

            if not simd.empty:
                simd_speedup = seq_time / simd['mean'].values[0]
                ax.axhline(y=simd_speedup, color='orange', linestyle='--',
                          label=f'SIMD ({simd_speedup:.2f}x)', linewidth=2)

            if not parallel_simd.empty:
                threads = parallel_simd['threads'].values
                times = parallel_simd['mean'].values
                speedups = seq_time / times

                ax.plot(threads, speedups, marker='o',
                       label='Parallel+SIMD', linewidth=2)

                ax.plot(threads, threads, 'k--', alpha=0.3, label='Linear')

        ax.set_xlabel('Threads')
        ax.set_ylabel('Speedup')
        ax.set_title(f'Tarefa C - Speedup (N={n})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log', base=2)

    plt.tight_layout()
    plt.savefig('tarefa_c_speedup.png', dpi=150)
    print("Gráfico salvo: tarefa_c_speedup.png")
    plt.close()

def plot_tarefa_d(stats):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    n_values = sorted(stats['n'].unique())

    for idx, n in enumerate(n_values):
        ax = axes[idx]

        data_n = stats[stats['n'] == n]

        ingenua = data_n[(data_n['tarefa'] == 'tarefa_d_ingenua')]
        otimizada = data_n[(data_n['tarefa'] == 'tarefa_d_otimizada')]

        if not ingenua.empty:
            threads = ingenua['threads'].values
            times = ingenua['mean'].values
            stds = ingenua['std'].values

            ax.errorbar(threads, times, yerr=stds, marker='o',
                       capsize=5, label='Ingênua (2x parallel for)', linewidth=2)

        if not otimizada.empty:
            threads = otimizada['threads'].values
            times = otimizada['mean'].values
            stds = otimizada['std'].values

            ax.errorbar(threads, times, yerr=stds, marker='s',
                       capsize=5, label='Otimizada (1x parallel)', linewidth=2)

        ax.set_xlabel('Threads')
        ax.set_ylabel('Tempo (s)')
        ax.set_title(f'Tarefa D - Organização (N={n})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log', base=2)

    plt.tight_layout()
    plt.savefig('tarefa_d_tempo.png', dpi=150)
    print("Gráfico salvo: tarefa_d_tempo.png")
    plt.close()

def plot_tarefa_d_overhead(stats):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    n_values = sorted(stats['n'].unique())

    for idx, n in enumerate(n_values):
        ax = axes[idx]

        data_n = stats[stats['n'] == n]

        ingenua = data_n[(data_n['tarefa'] == 'tarefa_d_ingenua')]
        otimizada = data_n[(data_n['tarefa'] == 'tarefa_d_otimizada')]

        if not ingenua.empty and not otimizada.empty:
            merged = pd.merge(ingenua, otimizada, on='threads', suffixes=('_ing', '_ot'))

            threads = merged['threads'].values
            overhead = ((merged['mean_ing'] - merged['mean_ot']) / merged['mean_ot']) * 100

            ax.plot(threads, overhead, marker='o', linewidth=2, color='red')
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)

        ax.set_xlabel('Threads')
        ax.set_ylabel('Overhead (%)')
        ax.set_title(f'Tarefa D - Overhead Ingênua vs Otimizada (N={n})')
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log', base=2)

    plt.tight_layout()
    plt.savefig('tarefa_d_overhead.png', dpi=150)
    print("Gráfico salvo: tarefa_d_overhead.png")
    plt.close()

def generate_summary_table(stats_a, stats_cd):
    print("\n=== RESUMO ESTATÍSTICO ===\n")

    print("TAREFA A - LAÇO IRREGULAR")
    print("-" * 100)
    print(stats_a.to_string(index=False))

    print("\n\nTAREFA C - SAXPY")
    print("-" * 80)
    tarefa_c = stats_cd[stats_cd['tarefa'].str.contains('tarefa_c')]
    print(tarefa_c.to_string(index=False))

    print("\n\nTAREFA D - ORGANIZAÇÃO DE REGIÃO PARALELA")
    print("-" * 80)
    tarefa_d = stats_cd[stats_cd['tarefa'].str.contains('tarefa_d')]
    print(tarefa_d.to_string(index=False))

    with open('summary.txt', 'w') as f:
        f.write("=== RESUMO ESTATÍSTICO ===\n\n")
        f.write("TAREFA A - LAÇO IRREGULAR\n")
        f.write("-" * 100 + "\n")
        f.write(stats_a.to_string(index=False))
        f.write("\n\n\nTAREFA C - SAXPY\n")
        f.write("-" * 80 + "\n")
        f.write(tarefa_c.to_string(index=False))
        f.write("\n\n\nTAREFA D - ORGANIZAÇÃO DE REGIÃO PARALELA\n")
        f.write("-" * 80 + "\n")
        f.write(tarefa_d.to_string(index=False))

    print("\n\nResumo salvo em: summary.txt")

def main():
    print("Carregando dados de results.csv...")
    df = load_data()

    print("Calculando estatísticas...")
    stats_a, stats_cd = calculate_stats(df)

    print("\nGerando gráficos...")

    # Tarefa A
    if not stats_a.empty:
        plot_tarefa_a_schedule_comparison(stats_a)
        plot_tarefa_a_best_configs(stats_a)

    # Tarefa C
    plot_tarefa_c(stats_cd)
    plot_tarefa_c_speedup(stats_cd)

    # Tarefa D
    plot_tarefa_d(stats_cd)
    plot_tarefa_d_overhead(stats_cd)

    generate_summary_table(stats_a, stats_cd)

    print("\nAnálise concluída!")

if __name__ == '__main__':
    main()
