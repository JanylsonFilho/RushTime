import time 
import numpy as np

def heuristic_h1(state):
    """ Conta veiculos bloqueando o carro X ate a saida"""
    linhas, colunas = np.where(state.matrix == 'X')
    if len(linhas) == 0: return 0

    row_x = linhas[0]
    col_last_x = np.max(colunas)
    caminho_ate_saida = state.matrix[row_x, col_last_x + 1:]
    blockers = set(caminho_ate_saida) - {'.'}

    return len(blockers)

class Node:
    """ Classe auxiliar para manter a estrutura da arvore de busca"""
    def __init__(self, state, parent, move_desc, g, h):
        self.state= state
        self.parent = parent
        self.move_desc = move_desc
        self.g = g
        self.h = h
        self.f = g + h
        self.children = []
        self.is_in_open = True

def solve(initial_state, max_memory=5000):
    """
    LMA* com limite de memória melhorado.
    
    Aumentamos max_memory de 2000 para 8000 porque:
    - O limite anterior estava muito agressivo
    - Removia nós promissores prematuramente
    - Causava soluções subótimas
    """
    start_time = time.time()
    root = Node(initial_state, None, None, 0, heuristic_h1(initial_state))

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
                "name": f"LMA* com Heurística de Bloqueadores (H1) - Memória: {max_memory}",
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
                    # CORRIGIDO: Atualiza e reinsere na open_list
                    existing_node.g = g
                    existing_node.parent = best_node
                    existing_node.move_desc = move_desc
                    existing_node.f = g + existing_node.h
                    
                    # Reinsere na open_list se não estiver lá
                    if not existing_node.is_in_open:
                        open_list.append(existing_node)
                        existing_node.is_in_open = True
                continue

            h = heuristic_h1(next_state)
            child_node = Node(next_state, best_node, move_desc, g, h)
            best_node.children.append(child_node)
            visited[state_hash] = child_node
            open_list.append(child_node)

        # MELHORADO: Política de descarte mais inteligente
        if len(visited) > max_memory:
            open_list.sort(key=lambda n: (n.f, -n.g))
            # Remove os nós com pior f-value (menos promissores)
            worst_leaf = open_list.pop(-1)
            worst_leaf.is_in_open = False

            del visited[worst_leaf.state.to_hash()]

            parent = worst_leaf.parent
            if parent:
                parent.f = max(parent.f, worst_leaf.f)

                if worst_leaf in parent.children:
                    parent.children.remove(worst_leaf)

                if not parent.children and not parent.is_in_open:
                    open_list.append(parent)
                    parent.is_in_open = True

    return None