from board_generator import get_board_from_bank, generate_random_state_from_final
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
    # ========== ESCOLHA O MODO ==========
    USAR_ESTADO_ALEATORIO = True
    NUM_MOVIMENTOS = 30 # Número de movimentos para gerar o estado inicial aleatório
    
    if USAR_ESTADO_ALEATORIO:
        print(f"[Gerando estado aleatório com {NUM_MOVIMENTOS} movimentos]")
        estado_comum = generate_random_state_from_final(num_moves=NUM_MOVIMENTOS)
    else:
        print("[Usando tabuleiro padrão do banco]")
        layout = get_board_from_bank(dificuldade="exemplo_pdf") 
        estado_comum = RushHourState(layout)
    
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
    res_lma_h1 = lma_star_h1_solve(estado_comum)  # Usa padrão melhorado: max_memory=8000
    imprimir_resultado(res_lma_h1)

    print("\n[ Executando LMA* (Heurística 2 - Distância) ]")
    res_lma_h2 = lma_star_h2_solve(estado_comum)  # Usa padrão: max_memory=5000
    imprimir_resultado(res_lma_h2)

    print("\n[ Executando A* (Heurística 3: Combinada) ]")
    res_h3 = astar_h3_solve(estado_comum)
    imprimir_resultado(res_h3)

    print("\n[ Executando LMA* (Heurística 3 - Combinada) ]")
    res_lma_h3 = lma_star_h3_solve(estado_comum)  # Usa padrão: max_memory=5000
    imprimir_resultado(res_lma_h3)

    print("\n[ Executando A* (Heurística 4: Dependências) ]")
    res_h4 = astar_h4_solve(estado_comum)
    imprimir_resultado(res_h4)

    print("\n[ Executando LMA* (Heurística 4 - Dependências) ]")
    res_lma_h4 = lma_star_h4_solve(estado_comum)  # Usa padrão: max_memory=5000
    imprimir_resultado(res_lma_h4)

if __name__ == "__main__":
    main()