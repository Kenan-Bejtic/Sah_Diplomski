import pygame
import os
from zvuk import Zvuk
from tema import Tema

class Konfiguracija:
    def __init__(self):
        pygame.font.init()  # Inicijaliziramo modul za fontove prije kreiranja fonta
        self.teme = []
        self._dodaj_teme()
        self.idx = 0
        self.tema = self.teme[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.zvuk_poteza = Zvuk(os.path.join('assets/sounds/potez.wav'))
        self.zvuk_hvatanja = Zvuk(os.path.join('assets/sounds/hvatanje.wav'))

    def promijeni_temu(self):
        self.idx += 1
        self.idx %= len(self.teme)
        self.tema = self.teme[self.idx]

    def _dodaj_teme(self):
        zelena = Tema((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        smeđa = Tema((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        plava = Tema((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        siva = Tema((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')
        self.teme = [zelena, smeđa, plava, siva]
