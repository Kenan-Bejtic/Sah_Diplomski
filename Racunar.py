# Modul Racunar.py (prethodni Computer.py)
import math
from Tabla import Tabla
from Figura import *
from functools import wraps
import random


PIJUN_TABLICA = [
    [0,   0,   0,   0,   0,   0,   0,  0],
    [50, 50,  50,  50,  50,  50,  50, 50],
    [10, 10,  20,  30,  30,  20,  10, 10],
    [5,   5,  10,  25,  25,  10,   5,  5],
    [0,   0,   0,  20,  20,   0,   0,  0],
    [5,  -5, -10,   0,   0, -10,  -5,  5],
    [5,  10,  10, -20, -20,  10,  10,  5],
    [0,   0,   0,   0,   0,   0,   0,  0]
]

# Konj (Knight) positional values
KONJ_TABLICA = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

# Lovac (Bishop) positional values
LOVAC_TABLICA = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

# Top (Rook) positional values
TOP_TABLICA = [
    [0,   0,  0,  0,  0,  0,  0,  0],
    [5,  10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,   0,  0,  5,  5,  0,  0,  0]
]

# Kraljica (Queen) positional values
KRALJICA_TABLICA = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [0,    0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

# Kralj (King) middlegame positional values 
KRALJ_TABLICA = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20,  20,  0,   0,  0,   0, 20, 20],
    [20,  30, 10,   0,  0,  10, 30, 20]
]



def minimax(tabla, dubina, alpha, beta, maks_igrac, spasi_potez, podaci):

    if dubina == 0 or tabla.zavrsena_igra():
        podaci[1] = tabla.procijeni()
        return podaci

    if maks_igrac:
        maks_procjena = -math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(tabla[i][j], Figura) and tabla[i][j].boja != tabla.dohvati_boju_igraca():
                    figura = tabla[i][j]
                    potezi = figura.filtriraj_poteze(figura.dohvati_poteze(tabla), tabla)
                    for potez in potezi:
                        tabla.izvrši_potez(figura, potez[0], potez[1], zadrži_povijest=True)
                        procjena = minimax(tabla, dubina - 1, alpha, beta, False, False, podaci)[1]
                        if spasi_potez:
                            if procjena >= maks_procjena:
                                if procjena > podaci[1]:
                                    podaci.clear()
                                    podaci[1] = procjena
                                    podaci[0] = [figura, potez, procjena]
                                elif procjena == podaci[1]:
                                    podaci[0].append([figura, potez, procjena])
                        tabla.poništi_potez(figura)
                        maks_procjena = max(maks_procjena, procjena)
                        alpha = max(alpha, procjena)
                        if beta <= alpha:
                            break
        return podaci
    else:
        min_procjena = math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(tabla[i][j], Figura) and tabla[i][j].boja == tabla.dohvati_boju_igraca():
                    figura = tabla[i][j]
                    potezi = figura.dohvati_poteze(tabla)
                    for potez in potezi:
                        tabla.izvrši_potez(figura, potez[0], potez[1], zadrži_povijest=True)
                        procjena = minimax(tabla, dubina - 1, alpha, beta, True, False, podaci)[1]
                        tabla.poništi_potez(figura)
                        min_procjena = min(min_procjena, procjena)
                        beta = min(beta, procjena)
                        if beta <= alpha:
                            break
        return podaci

def dohvati_ai_potez(tabla):
    potezi = minimax(tabla, tabla.dubina, -math.inf, math.inf, True, True, [[], 0])
    
    if len(potezi[0]) == 0:
        return False
    najbolja_procjena = max(potezi[0], key=lambda x: x[2])[2]
    figura_i_potez = random.choice([potez for potez in potezi[0] if potez[2] == najbolja_procjena])
    figura = figura_i_potez[0]
    potez = figura_i_potez[1]
    if isinstance(figura, Figura) and len(potez) > 0 and isinstance(potez, tuple):
        tabla.izvrši_potez(figura, potez[0], potez[1])
    return True

def dohvati_slucajni_potez(tabla):
    figure = []
    potezi_lista = []
    for i in range(8):
        for j in range(8):
            if isinstance(tabla[i][j], Figura) and tabla[i][j].boja != tabla.dohvati_boju_igraca():
                figure.append(tabla[i][j])
    for figura in figure[:]:
        potezi_figure = figura.filtriraj_poteze(figura.dohvati_poteze(tabla), tabla)
        if len(potezi_figure) == 0:
            figure.remove(figura)
        else:
            potezi_lista.append(potezi_figure)
    if len(figure) == 0:
        return
    figura = random.choice(figure)
    potez = random.choice(potezi_lista[figure.index(figura)])
    if isinstance(figura, Figura) and len(potez) > 0:
        tabla.izvrši_potez(figura, potez[0], potez[1])


def dohvati_pozicijsku_vrijednost(piece):
    """
    Returns the positional bonus for the piece based on its type and position.
    For white pieces, the table is used directly. For black pieces, the table is flipped vertically.
    """
    # Determine which table to use based on the piece type.
    if isinstance(piece, Pijun):
        table = PIJUN_TABLICA
    elif isinstance(piece, Konj):
        table = KONJ_TABLICA
    elif isinstance(piece, Lovac):
        table = LOVAC_TABLICA
    elif isinstance(piece, Top):
        table = TOP_TABLICA
    elif isinstance(piece, Kraljica):
        table = KRALJICA_TABLICA
    elif isinstance(piece, Kralj):
        table = KRALJ_TABLICA
    else:
        return 0

    # Use the piece's current coordinates (assumed to be stored in piece.x, piece.y)
    i, j = piece.x, piece.y

    # For white, use the table as is; for black, mirror the rows.
    if piece.boja == 'bijeli':
        return table[i][j]
    else:
        return table[7 - i][j]


# Here is an updated evaluation function for the board (in your Tabla class)
def procijeni(self):
    """
    Evaluates the board by summing the base piece values plus positional bonuses.
    Pieces belonging to the player (as returned by dohvati_boju_igraca()) are added,
    while the opponent's pieces are subtracted.
    """
    total = 0
    # Loop through each board cell (assuming an 8x8 board)
    for i in range(8):
        for j in range(8):
            piece = self[i][j]
            if isinstance(piece, Figura):
                # Base piece value (e.g. 10 for a pawn, 20 for a knight, etc.)
                base_value = piece.vrati_bodove()
                # Add the positional bonus from the piece–square table
                pos_bonus = dohvati_pozicijsku_vrijednost(piece)
                # Sum them together
                score = base_value + pos_bonus

                # If the piece is ours, add the score; if it's the opponent's, subtract it.
                if piece.boja == self.dohvati_boju_igraca():
                    total += score
                else:
                    total -= score
    return total