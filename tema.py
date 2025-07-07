from boja import Boja

class Tema:
    def __init__(self, pozadina_svijetla, pozadina_tamna, trag_svijetli, trag_tamni, potezi_svijetli, potezi_tamni):
        self.pozadina = Boja(pozadina_svijetla, pozadina_tamna)
        self.trag = Boja(trag_svijetli, trag_tamni)
        self.potezi = Boja(potezi_svijetli, potezi_tamni)
