import heapq
import time
import numpy as np

def heuristic_h1(state):
    """Conta veículos bloqueando o carro X até a saída[cite: 65, 67]."""
    # Encontra as coordenadas do X de uma só vez
    linhas, colunas = np.where(state.matrix == 'X')
    if len(linhas) == 0: return 0
    
    row_x = linhas[0]
    col_last_x = np.max(colunas)
    
    # Slicing: Pega o trecho da linha da frente do X até a saída [cite: 65]
    caminho_ate_saida = state.matrix[row_x, col_last_x + 1:]
    
    # Set mágico: retira os pontos e conta quantos carros únicos restaram [cite: 68]
    blockers = set(caminho_ate_saida) - {'.'}
    
    return len(blockers) 

def solve(initial_state):
    start_time = time.time()
    priority_queue = []
    count = 0 
    
    h_start = heuristic_h1(initial_state)
    heapq.heappush(priority_queue, (h_start, count, 0, initial_state, []))
    
    # Substituindo string por bytes via to_hash() para ficar mais rápido
    visited = {initial_state.to_hash(): 0}
    expanded_nodes = 0

    while priority_queue:
        f, _, g, current_state, path = heapq.heappop(priority_queue)
        expanded_nodes += 1

        if current_state.is_goal():
            return {
                "name": "A* com Heurística de Bloqueadores (H1)",
                "solution_path": path,
                "nodes_expanded": expanded_nodes,
                "time": time.time() - start_time,
                "cost": len(path),
                "depth": len(path)
            }

        for next_state, move_desc in current_state.get_successors():
            new_g = g + 1 
            state_hash = next_state.to_hash()
            
            if state_hash not in visited or new_g < visited[state_hash]:
                visited[state_hash] = new_g
                h = heuristic_h1(next_state)
                count += 1
                heapq.heappush(priority_queue, (new_g + h, count, new_g, next_state, path + [move_desc]))

    return None