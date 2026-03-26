import heapq
import time
import numpy as np

def heuristic_h4(state):
    """Combinação de Bloqueadores (H1) + Distância (H2) + Dependências."""

    # Quantos carros estao na frente + quanto falta andar + se esses veiculos estao presos por outros veiculos
    # cada bloqueador preso exige pelo menos 1 mov extra , ou seja , não superestima o custo
    matrix = state.matrix
    linhas, colunas = np.where(matrix == 'X')
    if len(linhas) == 0: return 0
    
    row_x = linhas[0]
    col_last_x = np.max(colunas)
    
    # 1. Distância
    distancia = 5 - col_last_x
    
    # 2. Bloqueadores Diretos
    caminho_ate_saida = matrix[row_x, col_last_x + 1:]
    blockers = set(caminho_ate_saida) - {'.'}
    
    h_val = distancia + len(blockers)
    
    # 3. Dependências (Blocker's Blockers)
    for blocker in blockers:
        # encontra as coordenadas dos veiculos que estao bloqueando X 
        coords = np.argwhere(matrix == blocker)
        if len(coords) == 0: continue
        
        row_start = np.min(coords[:, 0])
        row_end = np.max(coords[:, 0])
        col = coords[0, 1]
        
        # Verifica se o bloqueador consegue dar ao menos um passo para cima ou para baixo
        can_move_up = (row_start > 0) and (matrix[row_start - 1, col] == '.')
        can_move_down = (row_end < 5) and (matrix[row_end + 1, col] == '.')
        
        # Se ele não pode ir nem para cima nem para baixo, isso significa que o carro bloqueador esta preso , dependendo de terceiros 
        if not can_move_up and not can_move_down:
            h_val += 1
            
    return h_val

def solve(initial_state):
    start_time = time.time()
    priority_queue = []
    count = 0 
    
    h_start = heuristic_h4(initial_state)
    heapq.heappush(priority_queue, (h_start, count, 0, initial_state, []))
    
    visited = {initial_state.to_hash(): 0}
    expanded_nodes = 0

    while priority_queue:
        f, _, g, current_state, path = heapq.heappop(priority_queue)
        expanded_nodes += 1

        if current_state.is_goal():
            return {
                "name": "A* com Heurística de Dependências (H4)",
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
                h = heuristic_h4(next_state)
                count += 1
                heapq.heappush(priority_queue, (new_g + h, count, new_g, next_state, path + [move_desc]))

    return None