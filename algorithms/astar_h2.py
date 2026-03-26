import heapq 
import time 
import numpy as np

def heuristic_h2(state):
    """Calcula a distância restante do carro X até a saída"""
    _, colunas = np.where(state.matrix == 'X')
    if len(colunas) == 0: return 0

    # Localiza a parte mais à direita do carro X
    col_last_x = np.max(colunas)

    # A distância é as 5 colunas totais menos a coluna atual do carro
    distancia = 5 - col_last_x

    return distancia 

def solve(initial_state):
    start_time = time.time()
    priority_queue = []
    count = 0

    h_start = heuristic_h2(initial_state)
    heapq.heappush(priority_queue, (h_start, count, 0, initial_state, []))

    visited = {initial_state.to_hash(): 0}
    expanded_nodes = 0

    while priority_queue:
        f, _, g, current_state, path = heapq.heappop(priority_queue)
        expanded_nodes += 1

        if current_state.is_goal():
            return {
                "name": "A* com Heurística de Distância (H2)",
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
                h = heuristic_h2(next_state)
                count += 1
                heapq.heappush(priority_queue, (new_g + h, count, new_g, next_state, path + [move_desc]))

    return None