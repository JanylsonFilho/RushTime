# O objetivo principal agora é analisar o impacto das heurísticas e a eficiência da busca, 
# então manteremos apenas a matriz de exemplo do trabalho prático.

import random
from models import RushHourState

BANCO_INSTANCIAS = {
    "exemplo_pdf": [
        [
            "....AA",
            "..BBCC",
            "XX..FE",
            "GGHHFE",
            "DD.IFE",
            "...IJJ"
        ]
    ]
}

def get_board_from_bank(dificuldade="exemplo_pdf"):
    """
    Retorna o tabuleiro de exemplo do trabalho prático.
    A dificuldade padrão foi alterada para carregar direto a matriz de teste.
    """
    if dificuldade not in BANCO_INSTANCIAS:
        raise ValueError("Instância não encontrada no banco.")

    # Como só temos um tabuleiro nessa categoria, pegamos o índice 0
    board_strings = BANCO_INSTANCIAS[dificuldade][0]
    
    # Converte as strings em uma matriz 2D (lista de listas)
    matriz = [list(linha) for linha in board_strings]

    return matriz


def generate_random_state_from_final(num_moves, final_state=None, avoid_undo=True):
    """
    Gera um estado aleatório aplicando N movimentos a partir de um estado final.
    
    Esta abordagem garante que o estado gerado seja sempre solvível, pois cada 
    movimento é aplicado de forma válida a partir de um estado final conhecido.
    
    ⚠️ IMPORTANTE: Agora evita que movimentos se desfaçam!
    ====================================================
    Se você mover carro X para esquerda, o próximo movimento NÃO pode ser mover
    carro X para direita (que desfaría o movimento anterior). Isso garante que
    todos os N movimentos realmente contribuem para alterar o estado final.
    
    Args:
        num_moves (int): Número de movimentos aleatórios a aplicar (dificuldade)
        final_state (RushHourState, optional): Estado final customizado. 
                                                Se None, usa padrão (exemplo_pdf).
        avoid_undo (bool, default=True): Se True, evita movimentos que desfazem
                                         o movimento anterior. Recomendado: sempre True
    
    Returns:
        RushHourState: Estado aleatório gerado após aplicar num_moves movimentos
    
    Exemplo:
        >>> # Gera estado com 30 movimentos, sem refazer passos
        >>> estado = generate_random_state_from_final(num_moves=30)
        >>> print(estado)
    """
    
    # Se não houver estado final customizado, usa o estado padrão (exemplo_pdf)
    if final_state is None:
        board = get_board_from_bank(dificuldade="exemplo_pdf")
        current_state = RushHourState(board)
    else:
        current_state = final_state
    
    last_move_info = None  # Rastreia o último movimento para evitar undo
    
    # Aplica num_moves movimentos aleatórios válidos
    for move_count in range(num_moves):
        successors = current_state.get_successors()
        
        # Se não houver sucessores (deadlock - improvável), interrompe
        if not successors:
            print(f"Aviso: Nenhum movimento válido disponível após {move_count} movimentos.")
            break
        
        # Filtra sucessores para evitar desfazer o movimento anterior
        if avoid_undo and last_move_info is not None:
            last_vehicle = last_move_info['vehicle']
            last_direction = last_move_info['direction']
            
            # Calcula direção oposta (undo)
            opposite_directions = {
                'esquerda': 'direita',
                'direita': 'esquerda',
                'cima': 'baixo',
                'baixo': 'cima'
            }
            opposite_direction = opposite_directions.get(last_direction)
            
            # Filtra sucessores que não desfazem o movimento anterior
            filtered_successors = [
                (state, desc) for state, desc in successors
                if not (f"mover {last_vehicle}" in desc and opposite_direction in desc)
            ]
            
            # Se houver sucessores válidos (não-undo), usa a lista filtrada
            # Caso contrário, falls back para todos os sucessores
            if filtered_successors:
                successors = filtered_successors
            else:
                # Se todos os sucessores desfazem o movimento anterior,
                # permite refazer (situação rara, mas pode acontecer)
                pass
        
        # Escolhe um sucessor aleatório
        next_state, move_description = random.choice(successors)
        current_state = next_state
        
        # Rastreia o movimento atual para a próxima iteração
        if "mover " in move_description:
            # Extrai informações do movimento (ex: "mover B para esquerda")
            parts = move_description.split("mover ")[1].split(" para ")
            if len(parts) == 2:
                vehicle = parts[0]
                direction = parts[1]
                last_move_info = {
                    'vehicle': vehicle,
                    'direction': direction
                }
    
    return current_state


def generate_multiple_random_instances(num_instances, num_moves_range=(10, 50)):
    """
    Gera múltiplas instâncias aleatórias para testes de benchmark.
    
    Args:
        num_instances (int): Quantas instâncias aleatórias gerar
        num_moves_range (tuple): Tupla (min_moves, max_moves) para variar a dificuldade
    
    Returns:
        list: Lista de tuplas (RushHourState, num_moves_aplicados)
    
    Exemplo:
        >>> instancias = generate_multiple_random_instances(5, num_moves_range=(20, 40))
        >>> for estado, movimentos in instancias:
        ...     print(f"Instância com {movimentos} movimentos")
    """
    instances = []
    min_moves, max_moves = num_moves_range
    
    for i in range(num_instances):
        num_moves = random.randint(min_moves, max_moves)
        state = generate_random_state_from_final(num_moves=num_moves)
        instances.append((state, num_moves))
    
    return instances



# Testando a saída
if __name__ == "__main__":
    print("=== Teste 1: Tabuleiro padrão ===")
    tabuleiro = get_board_from_bank()
    for linha in tabuleiro:
        print(linha)
    
    print("\n=== Teste 2: Estado aleatório com 10 movimentos ===")
    estado_aleatorio = generate_random_state_from_final(num_moves=10)
    print(estado_aleatorio)
    
    print("\n=== Teste 3: Estado aleatório com 30 movimentos ===")
    estado_aleatorio_dificil = generate_random_state_from_final(num_moves=30)
    print(estado_aleatorio_dificil)