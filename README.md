# RushTime - Solucionador de Puzzle Rush Hour

## 📋 Descrição do Projeto

**RushTime** é um solucionador de puzzles Rush Hour que implementa múltiplos algoritmos de busca inteligente com diferentes heurísticas. O objetivo é encontrar a menor sequência de movimentos para sair com o carro amarelo (X) do tabuleiro 6x6.

O projeto compara a eficiência de diferentes abordagens:
- **BFS** (Breadth-First Search) - busca sem informação
- **A*** com 4 heurísticas distintas
- **LMA*** (Limited-Memory A*) com 4 heurísticas distintas

---

## 🗂️ Estrutura do Projeto

```
RushTime/
├── main.py                 # Ponto de entrada - executa todos os algoritmos
├── models.py              # Definição da classe RushHourState
├── board_generator.py     # Gerador de tabuleiros e estados aleatórios
├── README.md              # Este arquivo
├── algorithms/            # Pacote com todos os algoritmos
│   ├── __init__.py
│   ├── bfs_solver.py      # Busca em Largura (BFS)
│   ├── astar_h1.py        # A* com Heurística H1 (Bloqueadores)
│   ├── astar_h2.py        # A* com Heurística H2 (Avançada)
│   ├── astar_h3.py        # A* com Heurística H3 (Combinada)
│   ├── astar_h4.py        # A* com Heurística H4 (Dependências)
│   ├── lma_star_h1.py     # LMA* com Heurística H1
│   ├── lma_star_h2.py     # LMA* com Heurística H2
│   ├── lma_star_h3.py     # LMA* com Heurística H3
│   └── lma_star_h4.py     # LMA* com Heurística H4
└── __pycache__/           # Cache do Python
```

---

## 🎯 Componentes Principais

### 1. **models.py** - Representação do Estado do Puzzle

Define a classe `RushHourState` que representa o estado do tabuleiro:

```python
class RushHourState:
    def __init__(self, matrix):
        """Inicializa o estado com uma matriz 6x6"""
```

#### Métodos Principais:

| Método | Descrição |
|--------|-----------|
| `get_vehicles()` | Retorna dicionário com posições de todos os veículos |
| `get_successors()` | Gera todos os estados sucessores válidos (movimentos possíveis) |
| `is_goal()` | Verifica se o carro X está na posição de saída (coluna 5, linha 2) |
| `to_hash()` | Converte o estado para bytes para identificação única |
| `__repr__()` | Representação visual do tabuleiro |

**Características:**
- Tabuleiro representado como matriz NumPy 6x6
- Cada célula contém um caractere: veículo ou '.' (vazio)
- 'X' é o carro principal a ser liberado
- Movimentos são apenas 1 casa por vez
- Validação automática de movimentos legais

---

### 2. **board_generator.py** - Geração de Tabuleiros

Responsável por criar e gerenciar os estados iniciais.

#### Funções:

**`get_board_from_bank(dificuldade="exemplo_pdf")`**
- Retorna um tabuleiro pré-definido do banco de instâncias
- Atualmente contém apenas um exemplo: "exemplo_pdf"

**`generate_random_state_from_final(num_moves, final_state=None, avoid_undo=True)`**
- Gera estado aleatório aplicando N movimentos a partir do estado final
- **Garante que o estado é solucionável**
- `avoid_undo=True`: Evita desfazer movimentos anteriores
- Parâmetros:
  - `num_moves`: Quantidade de movimentos para gerar o estado (dificuldade)
  - `final_state`: Estado final customizado (padrão: exemplo_pdf)
  - `avoid_undo`: Se True, previne movimentos de undo

---

### 3. **main.py** - Orquestrador dos Algoritmos

Arquivo principal que executa todos os algoritmos de busca e exibe resultados.

#### Configurações:

```python
USAR_ESTADO_ALEATORIO = True    # True: estado aleatório | False: tabuleiro padrão
NUM_MOVIMENTOS = 30             # Número de movimentos para gerar estado aleatório
```

#### Função `imprimir_resultado(resultado)`
Exibe os resultados de cada algoritmo:
- Sequência de movimentos
- Número de estados expandidos
- Tempo de execução (segundos)
- Custo da solução (número de movimentos)

#### Ordem de Execução:
1. BFS (Breadth-First Search)
2. A* com H1 (Bloqueadores)
3. A* com H2 (Avançada)
4. LMA* com H1
5. LMA* com H2
6. A* com H3 (Combinada)
7. LMA* com H3
8. A* com H4 (Dependências)
9. LMA* com H4

---

## 🔍 Algoritmos Implementados

### BFS - Busca em Largura

**Arquivo:** `algorithms/bfs_solver.py`

- **Tipo:** Busca sem informação (uninformed search)
- **Completude:** Sim (sempre encontra solução)
- **Otimalidade:** Sim (encontra solução com menos movimentos)
- **Uso de Memorização:** Sim (rastreia estados visitados)

**Características:**
- Explora estados em ordem de profundidade
- Usa fila (FIFO - First In First Out)
- Serve como baseline para comparação
- Costuma expandir muitos nós

**Complexidade:**
- Tempo: O(b^d) onde b=branching factor, d=profundidade
- Espaço: O(b^d)

---

### A* (A-Star) - Busca Informada

Implementadas 4 versões com heurísticas diferentes.

#### **A* H1 - Heurística de Bloqueadores**

**Arquivo:** `algorithms/astar_h1.py`

```python
def heuristic_h1(state):
    """Conta veículos bloqueando o carro X até a saída"""
```

**Ideia:**
- Identifica o carro X na matriz
- Conta quantos veículos únicos estão bloqueando o caminho até a saída
- Quanto menos bloqueadores, mais perto da solução

**Exemplo:**
```
....AA
..BBCC      X está em (2,0) e (2,1)
XX..FE      Bloqueadores: F, E = 2 veículos
GGHHFE
DD.IFE
...IJJ
```

**Propriedades:**
- Heurística admissível (nunca superestima)
- Simples de calcular
- Muito eficiente para Rush Hour

---

#### **A* H2 - Heurística Avançada**

**Arquivo:** `algorithms/astar_h2.py`

- Versão mais sofisticada que combina múltiplas métricas
- Considera não apenas bloqueadores diretos, mas também dependências indiretas
- Geralmente melhor que H1 em termos de nós expandidos

---

#### **A* H3 - Heurística Combinada**

**Arquivo:** `algorithms/astar_h3.py`

- Combina aspectos das heurísticas anteriores
- Balanceamento entre precisão e tempo de cálculo
- Bom desempenho geral

---

#### **A* H4 - Heurística de Dependências**

**Arquivo:** `algorithms/astar_h4.py`

- Considera cadeias de dependência entre veículos
- Mais precisa mas computacionalmente mais cara
- Obtém melhor estimativa do custo restante

---

### LMA* - Limited-Memory A*

Implementadas 4 versões correspondentes às heurísticas do A*.

**Arquivo Exemplo:** `algorithms/lma_star_h1.py`

#### Características Principais:

```python
def solve(initial_state, max_memory=5000):
    """LMA* com limite de memória"""
```

**Diferenças do A*:**
- Limita o uso de memória com `max_memory`
- Remove nós menos promissores quando memória é excedida
- Útil para problemas com espaço de estados muito grande
- Pode encontrar soluções subótimas em casos extremos

**Parâmetros de Memória:**
- H1: `max_memory=8000` (mais agressivo)
- H2, H3, H4: `max_memory=5000` (padrão)

#### Estrutura Interna:

```python
class Node:
    """Representa nó na árvore de busca"""
    def __init__(self, state, parent, move_desc, g, h):
        self.state = state          # Estado do puzzle
        self.parent = parent        # Nó pai
        self.move_desc = move_desc  # Descrição do movimento
        self.g = g                  # Custo acumulado
        self.h = h                  # Valor heurístico
        self.f = g + h              # f(n) = g(n) + h(n)
        self.children = []          # Nós filhos
        self.is_in_open = True      # Se está na open list
```

---

## ▶️ Como Usar

### Pré-requisitos
```bash
pip install numpy
```

### Execução Básica

```bash
python main.py
```

### Configurar Estado Inicial

No arquivo `main.py`, modifique:

```python
# Usar estado aleatório (recomendado para testes)
USAR_ESTADO_ALEATORIO = True
NUM_MOVIMENTOS = 30

# OU usar tabuleiro padrão
USAR_ESTADO_ALEATORIO = False
```

### Usar Estado Customizado

```python
from models import RushHourState
from algorithms.astar_h1 import solve as astar_h1_solve

# Criar estado customizado
matriz = [
    "....AA",
    "..BBCC",
    "XX..FE",
    "GGHHFE",
    "DD.IFE",
    "...IJJ"
]
estado = RushHourState(matriz)

# Resolver
resultado = astar_h1_solve(estado)
print(resultado)
```

---

## 📊 Comparação de Algoritmos

| Algoritmo | Completude | Otimalidade | Velocidade | Memória | Uso |
|-----------|-----------|------------|-----------|---------|-----|
| BFS | Sim | Sim | Lenta | Alta | Baseline |
| A* H1 | Sim | Sim | Rápida | Normal | Recomendado |
| A* H2 | Sim | Sim | Muito Rápida | Normal | Bom |
| A* H3 | Sim | Sim | Rápida | Normal | Bom |
| A* H4 | Sim | Sim | Muito Rápida | Normal | Melhor |
| LMA* H1 | Sim* | Não* | Rápida | Baixa | Casos Grandes |
| LMA* H2 | Sim* | Não* | Rápida | Baixa | Casos Grandes |
| LMA* H3 | Sim* | Não* | Rápida | Baixa | Casos Grandes |
| LMA* H4 | Sim* | Não* | Rápida | Baixa | Casos Grandes |

*Com limite de memória: pode ser incompleto/subótimo em casos extremos

---

## 📈 Métricas Retornadas

Cada algoritmo retorna um dicionário com:

```python
{
    "name": str,              # Nome do algoritmo
    "solution_path": list,    # Lista de movimentos
    "nodes_expanded": int,    # Número de nós explorados
    "time": float,            # Tempo em segundos
    "cost": int,              # Número de movimentos
    "depth": int              # Profundidade da solução
}
```

---

## 🎓 Conceitos Principais

### Heurística
Função que estima o custo restante até o objetivo. Deve ser:
- **Admissível:** Nunca superestima o custo real
- **Consistente:** Mantém monotonicidade

### F(n) = G(n) + H(n)
- **G(n):** Custo acumulado do início até n
- **H(n):** Heurística (estimativa de custo restante)
- **F(n):** Estimativa do custo total através de n

### Estados Visitados
Conjunto que armazena hashes de estados já explorados para não repetir nós.

### Limite de Memória (LMA*)
Estratégia para controlar crescimento exponencial da memória removendo nós menos promissores.

---

## 🔧 Extensibilidade

### Adicionar Nova Heurística

1. Criar arquivo `algorithms/astar_h5.py`:

```python
def heuristic_h5(state):
    """Descrição da heurística H5"""
    # Implementar cálculo heurístico
    return valor

def solve(initial_state):
    # Implementar A* com H5
    pass
```

2. Importar em `main.py`:

```python
from algorithms.astar_h5 import solve as astar_h5_solve
```

3. Executar nos testes:

```python
res_h5 = astar_h5_solve(estado_comum)
imprimir_resultado(res_h5)
```

### Adicionar Novo Tabuleiro

Em `board_generator.py`:

```python
BANCO_INSTANCIAS = {
    "exemplo_pdf": [...],
    "novo_tabuleiro": [
        [
            "......",
            "......",
            "XX....",
            "......",
            "......",
            "......"
        ]
    ]
}
```

---

## 📝 Formato de Movimento

Cada movimento é descrito como:
```
mover {veículo} para {direção}

Exemplo:
mover X para direita
mover A para cima
mover B para esquerda
```

---

## 🐛 Troubleshooting

### "Nenhuma solução encontrada"
- Verifique se o tabuleiro é solucionável
- Aumente `NUM_MOVIMENTOS` se usar estado aleatório

### Algoritmo muito lento
- Use A* em vez de BFS
- Tente heurísticas H2, H3 ou H4
- Considere LMA* para espaços muito grandes

### Erro de Memória
- Use LMA* com `max_memory` apropriado
- Reduza `NUM_MOVIMENTOS` do estado inicial

---

## 📚 Referências

- **A* Algorithm:** Hart, P. E., Nilsson, N. J., & Raphael, B. (1968)
- **Limited-Memory A*:** Korf, R. E. (1992)
- **Rush Hour Puzzle:** Solver et al.

---

## 👤 Autor

Desenvolvimento do projeto RushTime

---

## 📄 Licença

[Especificar licença conforme necessário]

---

## 📝 Changelog

### Versão 1.0
- ✅ Implementação de BFS
- ✅ Implementação de A* com 4 heurísticas
- ✅ Implementação de LMA* com 4 heurísticas
- ✅ Gerador de estados aleatórios
- ✅ Sistema de avaliação comparativo