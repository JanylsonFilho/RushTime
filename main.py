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

def imprimir_resultado(resultado):
    if not resultado:
        print("Nenhuma solução encontrada.")
        return

    print("Solução encontrada!")
    print(f"Movimentos: {resultado['cost']}")
    
    # Imprime a sequência de movimentos
    for i, passo in enumerate(resultado['solution_path'], 1):
        print(f"{i} {passo}")

    # Imprime as estatísticas de busca
    print("\n--- Estatísticas de busca ---")
    print(f"Número de estados expandidos: {resultado['nodes_expanded']}")
    print(f"Tempo de execução: {resultado['time']:.4f} s")
    print(f"Custo da solução: {resultado['cost']}")
    print("-" * 30)

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

    # 2. Executa os algoritmos
    print("\n[ Executando Busca em Largura (BFS) ]")
    res_bfs = bfs_solve(estado_comum)
    imprimir_resultado(res_bfs)

    print("\n[ Executando A* (Heurística 1: Bloqueadores) ]")
    res_h1 = astar_h1_solve(estado_comum)
    imprimir_resultado(res_h1)

    print("\n[ Executando A* (Heurística 2: Avançada) ]")
    res_h2 = astar_h2_solve(estado_comum)
    imprimir_resultado(res_h2)

    print("\n[ Executando LMA* (Heurística 1 - Bloqueadores) ]")
    res_lma_h1 = lma_star_h1_solve(estado_comum)
    imprimir_resultado(res_lma_h1)

    print("\n[ Executando LMA* (Heurística 2 - Distância) ]")
    res_lma_h2 = lma_star_h2_solve(estado_comum)
    imprimir_resultado(res_lma_h2)

    print("\n[ Executando A* (Heurística 3: Combinada) ]")
    res_h3 = astar_h3_solve(estado_comum)
    imprimir_resultado(res_h3)

    print("\n[ Executando LMA* (Heurística 3 - Combinada) ]")
    res_lma_h3 = lma_star_h3_solve(estado_comum)
    imprimir_resultado(res_lma_h3)

    print("\n[ Executando A* (Heurística 4: Dependências) ]")
    res_h4 = astar_h4_solve(estado_comum)
    imprimir_resultado(res_h4)

    print("\n[ Executando LMA* (Heurística 4 - Dependências) ]")
    res_lma_h4 = lma_star_h4_solve(estado_comum)
    imprimir_resultado(res_lma_h4)

if __name__ == "__main__":
    main()