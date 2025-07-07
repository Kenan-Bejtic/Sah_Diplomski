import pygame
import os

if not pygame.mixer.get_init():
    pygame.mixer.init()

class Zvuk:
    def __init__(self, putanja):
        self.putanja = putanja
        self.zvuk = pygame.mixer.Sound(putanja)

    def pusti(self):
        pygame.mixer.Sound.play(self.zvuk)
