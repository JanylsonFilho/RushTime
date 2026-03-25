import random

# 5 Puzzles 100% testados e com solução (convertidos para matrizes de caracteres).
PUZZLES = [
    [ # Puzzle 1 (Fácil) - 4 movimentos
        list("AA...B"),
        list("C....B"),
        list("CXX..B"),
        list("..DDEE"),
        list("......"),
        list("FFF...")
    ],
    [ # Puzzle 2 (Médio) - Requer manobra de 1 bloqueador
        list("AA..B."),
        list("F...B."),
        list("FXX.B."),
        list(".CC.DD"),
        list("...E.."),
        list("...E..")
    ],
    [ # Puzzle 3 (Médio) - Limpeza de caminho horizontal e vertical
        list(".AA..."),
        list("...BCC"),
        list("XX.B.."),
        list(".DDEEE"),
        list("...FGG"),
        list("...FHH")
    ],
    [ # Puzzle 4 (Difícil) - Congestionamento pesado no lado direito
        list("AABBB."),
        list("..C..D"),
        list("XXC..D"),
        list("..C.ED"),
        list("FF..E."),
        list("....E.")
    ],
    [ # Puzzle 5 (Expert) - Requer mover peças de volta para o lugar original
        list("AA.B.C"),
        list("D..B.C"),
        list("DXX..C"),
        list("DEEFFF"),
        list("...G.."),
        list("...G..")
    ]
]

def obter_mapa_aleatorio():
    """
    Seleciona um puzzle aleatoriamente e retorna uma cópia dele.
    Retorna uma tupla contendo o (indice_do_puzzle, matriz_do_estado_inicial).
    """
    index = random.randint(0, len(PUZZLES) - 1)
    
    # Criamos uma cópia do tabuleiro para que os algoritmos não alterem o mapa original (PUZZLES)
    estado_inicial = [linha[:] for linha in PUZZLES[index]]
    
    return index, estado_inicial