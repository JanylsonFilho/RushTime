from board_generator import obter_mapa_aleatorio  # Como você já colocou no board_generator
from models import RushHourState
from algorithms.bfs_solver import solve as bfs_solve
from algorithms.astar_h1 import solve as astar_h1_solve
from algorithms.astar_h2 import solve as astar_h2_solve
from algorithms.lma_star_h1 import solve as lma_star_h1_solve
from algorithms.lma_star_h2 import solve as lma_star_h2_solve
from algorithms.astar_h3 import solve as astar_h3_solve
from algorithms.lma_star_h3 import solve as lma_star_h3_solve
from algorithms.astar_h4 import solve as astar_h4_solve
from algorithms.lma_star_h4 import solve as lma_star_h4_solve
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def imprimir_resultado(resultado):
    if not resultado:
        print("Nenhuma solução encontrada.")
        return

    print("Solução encontrada!")
    print(f"Movimentos: {resultado['cost']}")
    
    # Imprime a sequência de movimentos
    for i, passo in enumerate(resultado['solution_path'], 1):
        print(f"{i} {passo}")

    # Imprime as estatísticas de busca em milissegundos
    print("\n--- Estatísticas de busca ---")
    print(f"Número de estados expandidos: {resultado['nodes_expanded']}")
    tempo_ms = resultado['time'] * 1000  # Converter para milissegundos
    print(f"Tempo de execução: {tempo_ms:.2f} ms")
    print(f"Custo da solução: {resultado['cost']}")
    print("-" * 30)

def gerar_graficos_comparativos(resultados_dict):
    """
    Gera gráficos comparativos de desempenho entre os algoritmos.
    Salva as imagens em um diretório 'images' com timestamp para evitar sobrescrita.
    
    Args:
        resultados_dict: Dicionário com nome do algoritmo -> resultado
    """
    
    # Filtra apenas resultados válidos (com solução encontrada)
    resultados_validos = {nome: res for nome, res in resultados_dict.items() if res is not None}
    
    if not resultados_validos:
        print("⚠️  Nenhum resultado válido para gerar gráficos")
        return
    
    # Criar diretório 'images' se não existir
    if not os.path.exists('images'):
        os.makedirs('images')
        print("✅ Diretório 'images/' criado com sucesso!")
    
    nomes_algoritmos = list(resultados_validos.keys())
    estados_expandidos = [resultados_validos[nome]['nodes_expanded'] for nome in nomes_algoritmos]
    tempos_execucao_ms = [resultados_validos[nome]['time'] * 1000 for nome in nomes_algoritmos]  # Converter para ms
    
    # ===== CALCULAR PORCENTAGEM COMPARADA AO BFS =====
    bfs_estados = resultados_validos['BFS']['nodes_expanded']
    economia_percentual = [(bfs_estados - estados) / bfs_estados * 100 for estados in estados_expandidos]
    
    # Criar figura com 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('Comparação Completa de Desempenho dos Algoritmos de Busca', fontsize=16, fontweight='bold')
    
    # ===== GRÁFICO 1: Estados Expandidos =====
    cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA15E', '#BC6C25', '#8E44AD', '#E74C3C']
    
    bars1 = axes[0].bar(range(len(nomes_algoritmos)), estados_expandidos, color=cores[:len(nomes_algoritmos)], edgecolor='black', linewidth=1.5)
    axes[0].set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Número de Estados Expandidos', fontsize=12, fontweight='bold')
    axes[0].set_title('Estados Expandidos (Menor = Melhor)', fontsize=13, fontweight='bold')
    axes[0].set_xticks(range(len(nomes_algoritmos)))
    axes[0].set_xticklabels(nomes_algoritmos, rotation=45, ha='right')
    axes[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar valores nas barras
    for bar, valor in zip(bars1, estados_expandidos):
        altura = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., altura,
                    f'{int(valor)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # ===== GRÁFICO 2: Tempo de Execução em Milissegundos =====
    bars2 = axes[1].bar(range(len(nomes_algoritmos)), tempos_execucao_ms, color=cores[:len(nomes_algoritmos)], edgecolor='black', linewidth=1.5)
    axes[1].set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Tempo de Execução (milissegundos)', fontsize=12, fontweight='bold')
    axes[1].set_title('Tempo de Execução em ms (Menor = Melhor)', fontsize=13, fontweight='bold')
    axes[1].set_xticks(range(len(nomes_algoritmos)))
    axes[1].set_xticklabels(nomes_algoritmos, rotation=45, ha='right')
    axes[1].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar valores nas barras
    for bar, valor in zip(bars2, tempos_execucao_ms):
        altura = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., altura,
                    f'{valor:.2f}ms',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # ===== GRÁFICO 3: Gráfico de Pizza - Economia comparada ao BFS =====
    # Filtra apenas algoritmos que tiveram economia (exclui BFS que é a referência com 0%)
    nomes_para_pizza = [nome for nome in nomes_algoritmos if nome != 'BFS']
    economia_para_pizza = [economia_percentual[nomes_algoritmos.index(nome)] for nome in nomes_para_pizza]
    cores_pizza = [cores[nomes_algoritmos.index(nome)] for nome in nomes_para_pizza]
    
    # Criar pizza
    wedges, texts, autotexts = axes[2].pie(economia_para_pizza, 
                                             labels=nomes_para_pizza,
                                             autopct='%1.1f%%',
                                             colors=cores_pizza,
                                             startangle=90,
                                             textprops={'fontsize': 9, 'fontweight': 'bold'})
    
    # Melhorar formato dos percentuais
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(8)
        autotext.set_fontweight('bold')
    
    axes[2].set_title('Economia de Expansões\nComparado ao BFS', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    
    # Gerar nome único com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f'images/comparacao_algoritmos_{timestamp}.png'
    
    # Salvar figura
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico salvo como: {nome_arquivo}")
    
    # Exibir figura
    plt.show()
    
    # ===== Tabela Resumida =====
    print("\n" + "="*110)
    print("TABELA RESUMIDA DE DESEMPENHO")
    print("="*110)
    print(f"{'Algoritmo':<30} {'Estados':<15} {'Tempo (ms)':<18} {'Economia vs BFS':<20} {'Custo':<10}")
    print("-"*110)
    for idx, nome in enumerate(nomes_algoritmos):
        tempo_ms = resultados_validos[nome]['time'] * 1000
        economia = economia_percentual[idx]
        economia_str = f"{economia:.1f}%" if economia > 0 else "Referência"
        print(f"{nome:<30} {resultados_validos[nome]['nodes_expanded']:<15} {tempo_ms:<18.2f} {economia_str:<20} {resultados_validos[nome]['cost']:<10}")
    print("="*110)
    
    # Listar todas as imagens salvas
    print("\n📁 Imagens salvas no diretório 'images/':")
    imagens = sorted([f for f in os.listdir('images') if f.endswith('.png')])
    for idx, imagem in enumerate(imagens, 1):
        print(f"   {idx}. {imagem}")

def main():
    # 1. Obtém o mapa aleatório da nova estrutura
    index, matriz_inicial = obter_mapa_aleatorio()
    
    print(f"[ Usando Puzzle Sorteado: {index + 1} ]")
    
    # Passamos matriz_inicial DIRETAMENTE para a classe, sem converter para string
    # Isso fará o numpy criar uma matriz 2D (6x6) corretamente.
    estado_comum = RushHourState(matriz_inicial)
    
    print("\nConfiguração Inicial:")
    print(estado_comum)
    print("-" * 20)

    # Dicionário para coletar resultados
    resultados = {}

    # 2. Executa os algoritmos
    print("\n[ Executando Busca em Largura (BFS) ]")
    res_bfs = bfs_solve(estado_comum)
    imprimir_resultado(res_bfs)
    resultados['BFS'] = res_bfs

    print("\n[ Executando A* (Heurística 1: Bloqueadores) ]")
    res_h1 = astar_h1_solve(estado_comum)
    imprimir_resultado(res_h1)
    resultados['A* H1'] = res_h1

    print("\n[ Executando A* (Heurística 2: Avançada) ]")
    res_h2 = astar_h2_solve(estado_comum)
    imprimir_resultado(res_h2)
    resultados['A* H2'] = res_h2

    print("\n[ Executando LMA* (Heurística 1 - Bloqueadores) ]")
    res_lma_h1 = lma_star_h1_solve(estado_comum)
    imprimir_resultado(res_lma_h1)
    resultados['LMA* H1'] = res_lma_h1

    print("\n[ Executando LMA* (Heurística 2 - Distância) ]")
    res_lma_h2 = lma_star_h2_solve(estado_comum)
    imprimir_resultado(res_lma_h2)
    resultados['LMA* H2'] = res_lma_h2

    print("\n[ Executando A* (Heurística 3: Combinada) ]")
    res_h3 = astar_h3_solve(estado_comum)
    imprimir_resultado(res_h3)
    resultados['A* H3'] = res_h3

    print("\n[ Executando LMA* (Heurística 3 - Combinada) ]")
    res_lma_h3 = lma_star_h3_solve(estado_comum)
    imprimir_resultado(res_lma_h3)
    resultados['LMA* H3'] = res_lma_h3

    print("\n[ Executando A* (Heurística 4: Dependências) ]")
    res_h4 = astar_h4_solve(estado_comum)
    imprimir_resultado(res_h4)
    resultados['A* H4'] = res_h4

    print("\n[ Executando LMA* (Heurística 4 - Dependências) ]")
    res_lma_h4 = lma_star_h4_solve(estado_comum)
    imprimir_resultado(res_lma_h4)
    resultados['LMA* H4'] = res_lma_h4
    
    # 3. Gera gráficos comparativos
    print("\n" + "="*80)
    print("GERANDO GRÁFICOS COMPARATIVOS...")
    print("="*80)
    gerar_graficos_comparativos(resultados)

if __name__ == "__main__":
    main()