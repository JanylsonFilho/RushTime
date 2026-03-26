import time
import numpy as np

def heuristic_h4(state):
    """Combinação de Bloqueadores (H1) + Distância (H2) + Dependências."""
    matrix = state.matrix
    linhas, colunas = np.where(matrix == 'X')
    if len(linhas) == 0: return 0
    
    row_x = linhas[0]
    col_last_x = np.max(colunas)
    
    distancia = 5 - col_last_x
    caminho_ate_saida = matrix[row_x, col_last_x + 1:]
    blockers = set(caminho_ate_saida) - {'.'}
    
    h_val = distancia + len(blockers)
    
    for blocker in blockers:
        coords = np.argwhere(matrix == blocker)
        if len(coords) == 0: continue
        
        row_start = np.min(coords[:, 0])
        row_end = np.max(coords[:, 0])
        col = coords[0, 1]
        
        can_move_up = (row_start > 0) and (matrix[row_start - 1, col] == '.')
        can_move_down = (row_end < 5) and (matrix[row_end + 1, col] == '.')
        
        if not can_move_up and not can_move_down:
            h_val += 1
            
    return h_val

class Node:
    def __init__(self, state, parent, move_desc, g, h):
        self.state = state
        self.parent = parent
        self.move_desc = move_desc
        self.g = g
        self.h = h
        self.f = g + h
        self.children = []
        self.is_in_open = True

def solve(initial_state, max_memory=5000):
    """LMA* com limite de memória melhorado (H4 - Dependências)."""
    start_time = time.time()
    root = Node(initial_state, None, None, 0, heuristic_h4(initial_state))
    
    open_list = [root]
    visited = {initial_state.to_hash(): root}
    expanded_nodes = 0

    while open_list:
        open_list.sort(key=lambda n: (n.f, -n.g))
        best_node = open_list.pop(0)
        best_node.is_in_open = False
        expanded_nodes += 1

        if best_node.state.is_goal():
            path = []
            curr = best_node
            while curr.parent:
                path.append(curr.move_desc)
                curr = curr.parent
            return {
                "name": f"LMA* com Heurística de Dependências (H4) - Memória: {max_memory}",
                "solution_path": path[::-1],
                "nodes_expanded": expanded_nodes,
                "time": time.time() - start_time,
                "cost": len(path),
                "depth": len(path)
            }

        for next_state, move_desc in best_node.state.get_successors():
            state_hash = next_state.to_hash()
            g = best_node.g + 1
            
            if state_hash in visited:
                existing_node = visited[state_hash]
                if g < existing_node.g:
                    existing_node.g = g
                    existing_node.parent = best_node
                    existing_node.move_desc = move_desc
                    existing_node.f = g + existing_node.h
                    
                    if not existing_node.is_in_open:
                        open_list.append(existing_node)
                        existing_node.is_in_open = True
                continue
            
            h = heuristic_h4(next_state)
            child_node = Node(next_state, best_node, move_desc, g, h)
            best_node.children.append(child_node)
            visited[state_hash] = child_node
            open_list.append(child_node)
            
        while len(visited) > max_memory:
            open_list.sort(key=lambda n: (n.f, -n.g))
            worst_leaf = open_list.pop(-1)
            worst_leaf.is_in_open = False
            
            del visited[worst_leaf.state.to_hash()]
            
            parent = worst_leaf.parent
            if parent:
                # Remove o filho ruim da lista de filhos do pai
                if worst_leaf in parent.children:
                    parent.children.remove(worst_leaf)

                # A CORREÇÃO DA LÓGICA ESTÁ AQUI:
                if parent.children:
                    # Se o pai ainda tem outros filhos na memória, 
                    # o custo dele é o custo do MELHOR filho restante.
                    parent.f = min(child.f for child in parent.children)
                else:
                    # Se este era o último/único filho do pai, o pai
                    # herda esse custo ruim para não esquecer quão ruim era
                    # (garante que ele não seja re-expandido imediatamente)
                    parent.f = max(parent.f, worst_leaf.f)
                
                # Se o pai ficou sem filhos na memória e não está na fila,
                # ele volta para a fila para poder ser re-expandido no futuro
                if not parent.children and not parent.is_in_open:
                    open_list.append(parent)
                    parent.is_in_open = True

    return None