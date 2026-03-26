import numpy as np

class RushHourState:
    def __init__(self, matrix):
        # Converte a entrada para um array do numpy
        self.matrix = np.array(matrix, dtype=str)

    def get_vehicles(self):
        vehicles = {}
        unique_chars = np.unique(self.matrix)
        for char in unique_chars:
            if char != '.':
                # np.argwhere retorna as coordenadas exatas do veículo
                vehicles[char] = np.argwhere(self.matrix == char).tolist()
        return vehicles

    def get_successors(self):
        successors = []
        vehicles = self.get_vehicles()
        
        for vid, pos in vehicles.items():
            is_horiz = pos[0][0] == pos[-1][0]
            
            if is_horiz:
                row = pos[0][0]
                col_start = pos[0][1]
                col_end = pos[-1][1]
                
                # Esquerda (Apenas 1 casa)
                if col_start > 0 and self.matrix[row, col_start - 1] == '.':
                    successors.append((self._move(vid, pos, (0, -1)), f"mover {vid} para esquerda"))
                
                # Direita (Apenas 1 casa)
                if col_end < 5 and self.matrix[row, col_end + 1] == '.':
                    successors.append((self._move(vid, pos, (0, 1)), f"mover {vid} para direita"))
            else:
                col = pos[0][1]
                row_start = pos[0][0]
                row_end = pos[-1][0]
                
                # Cima (Apenas 1 casa)
                if row_start > 0 and self.matrix[row_start - 1, col] == '.':
                    successors.append((self._move(vid, pos, (-1, 0)), f"mover {vid} para cima"))
                
                # Baixo (Apenas 1 casa)
                if row_end < 5 and self.matrix[row_end + 1, col] == '.':
                    successors.append((self._move(vid, pos, (1, 0)), f"mover {vid} para baixo"))
                    
        return successors

    def _move(self, vid, pos, delta):
        new_matrix = self.matrix.copy()
        
        for r, c in pos: 
            new_matrix[r, c] = '.'
        # Essa linha pega cada celula do veiculo e reposiciona ela no tabuleiro somando o delta , que é o deslocamento
        for r, c in pos: 
            new_matrix[r + delta[0], c + delta[1]] = vid
            
        return RushHourState(new_matrix)

    def is_goal(self):
        return np.any(self.matrix[:, 5] == 'X')

    def to_hash(self):
        return self.matrix.tobytes()

    def __repr__(self):
        return "\n".join(" ".join(row) for row in self.matrix)