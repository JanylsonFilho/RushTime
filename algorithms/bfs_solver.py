import collections
import time

def solve(initial_state):
    start_time = time.time()
    queue = collections.deque([(initial_state, [])])
    
    # Aplicando o hash nativo para otimizar busca no set
    visited = {initial_state.to_hash()}
    expanded_nodes = 0

    while queue:
        current_state, path = queue.popleft()
        expanded_nodes += 1

        if current_state.is_goal():
            return {
                "name": "Busca em Largura (BFS)",
                "solution_path": path,
                "nodes_expanded": expanded_nodes,
                "time": time.time() - start_time,
                "cost": len(path),
                "depth": len(path)
            }

        for next_state, move_desc in current_state.get_successors():
            state_hash = next_state.to_hash()
            
            if state_hash not in visited:
                visited.add(state_hash)
                queue.append((next_state, path + [move_desc]))

        if expanded_nodes % 100 == 0:
            print(f"Expandidos: {expanded_nodes} ", end="\r")

    return None