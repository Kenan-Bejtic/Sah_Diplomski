# Modul Figura.py (prethodni ChessPiece.py)
import operator
from itertools import product

class Figura:
    # Povijest se koristi za čuvanje podataka, kako bi tabla.poništi_potez() radila ispravno.
    povijest_pojedenih_figura = []
    povijest_pomaknutih = []
    povijest_pozicija = []

    def __init__(self, boja, x, y, unicode):
        self.pomaknuta = False
        self.boja = boja
        self.x = x
        self.y = y
        self.tip = self.__class__.__name__
        self.unicode = unicode

    def filtriraj_poteze(self, potezi, tabla):
        konačni_potezi = potezi[:]
        for potez in potezi:
            tabla.izvrši_potez(self, potez[0], potez[1], zadrži_povijest=True)
            if tabla.kralj_je_ugrožen(self.boja, potez):
                konačni_potezi.remove(potez)
            tabla.poništi_potez(self)
        return konačni_potezi

    def dohvati_poteze(self, tabla):
        pass

    def dohvati_posljednju_pojedenu(self):
        return self.povijest_pojedenih_figura.pop()

    def postavi_posljednju_pojedenu(self, figura):
        self.povijest_pojedenih_figura.append(figura)

    def postavi_poziciju(self, x, y, zadrži_povijest):
        if zadrži_povijest:
            self.povijest_pozicija.append(self.x)
            self.povijest_pozicija.append(self.y)
            self.povijest_pomaknutih.append(self.pomaknuta)
        self.x = x
        self.y = y
        self.pomaknuta = True

    def vrati_starupoziciju(self):
        pozicija_y = self.povijest_pozicija.pop()
        pozicija_x = self.povijest_pozicija.pop()
        self.y = pozicija_y
        self.x = pozicija_x
        self.pomaknuta = self.povijest_pomaknutih.pop()

    def vrati_bodove(self):
        return 0

    def __repr__(self):
        return '{}: {}|{},{}'.format(self.tip, self.boja, self.x, self.y)


class Pijun(Figura):

    def dohvati_poteze(self, tabla):
        potezi = []
        if tabla.nacin_igre == 0 and self.boja == 'bijeli' or tabla.nacin_igre == 1 and self.boja == 'crni':
            smjer = 1
        else:
            smjer = -1
        x = self.x + smjer
        if tabla.prazno_polje(x, self.y):
            potezi.append((x, self.y))
            if self.pomaknuta is False and tabla.prazno_polje(x + smjer, self.y):
                potezi.append((x + smjer, self.y))
        if tabla.je_validan_potez(x, self.y - 1):
            if tabla.ima_protivnika(self, x, self.y - 1):
                potezi.append((x, self.y - 1))
        if tabla.je_validan_potez(self.x + smjer, self.y + 1):
            if tabla.ima_protivnika(self, x, self.y + 1):
                potezi.append((x, self.y + 1))
        return potezi

    def vrati_bodove(self):
        return 10




class Konj(Figura):

    def dohvati_poteze(self, tabla):
        potezi = []
        add = operator.add
        sub = operator.sub
        lista_op = [(add, sub), (sub, add), (add, add), (sub, sub)]
        brojevi = [(1, 2), (2, 1)]
        kombinacije = list(product(lista_op, brojevi))
        for komb in kombinacije:
            x = komb[0][0](self.x, komb[1][0])
            y = komb[0][1](self.y, komb[1][1])
            if tabla.prazno_polje(x, y) or tabla.ima_protivnika(self, x, y):
                potezi.append((x, y))
        return potezi

    def vrati_bodove(self):
        return 20
    

class Lovac(Figura):

    def dohvati_poteze(self, tabla):
        potezi = []
        add = operator.add
        sub = operator.sub
        operateri = [(add, add), (add, sub), (sub, add), (sub, sub)]
        for ops in operateri:
            for i in range(1, 9):
                x = ops[0](self.x, i)
                y = ops[1](self.y, i)
                if not tabla.je_validan_potez(x, y) or tabla.ima_prijatelja(self, x, y):
                    break
                if tabla.prazno_polje(x, y):
                    potezi.append((x, y))
                if tabla.ima_protivnika(self, x, y):
                    potezi.append((x, y))
                    break
        return potezi

    def vrati_bodove(self):
        return 30
    

class Top(Figura):

    def dohvati_poteze(self, tabla):
        potezi = []
        potezi += self.dohvati_vertikalne_poteze(tabla)
        potezi += self.dohvati_horizontalne_poteze(tabla)
        return potezi

    def dohvati_vertikalne_poteze(self, tabla):
        potezi = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                x = op(self.x, i)
                if not tabla.je_validan_potez(x, self.y) or tabla.ima_prijatelja(self, x, self.y):
                    break
                if tabla.prazno_polje(x, self.y):
                    potezi.append((x, self.y))
                if tabla.ima_protivnika(self, x, self.y):
                    potezi.append((x, self.y))
                    break
        return potezi

    def dohvati_horizontalne_poteze(self, tabla):
        potezi = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                y = op(self.y, i)
                if not tabla.je_validan_potez(self.x, y) or tabla.ima_prijatelja(self, self.x, y):
                    break
                if tabla.prazno_polje(self.x, y):
                    potezi.append((self.x, y))
                if tabla.ima_protivnika(self, self.x, y):
                    potezi.append((self.x, y))
                    break
        return potezi

    def vrati_bodove(self):
        return 30
    


class Kraljica(Figura):

    def dohvati_poteze(self, tabla):
        potezi = []
        top = Top(self.boja, self.x, self.y, self.unicode)
        lovac = Lovac(self.boja, self.x, self.y, self.unicode)
        potezi_topa = top.dohvati_poteze(tabla)
        potezi_lovca = lovac.dohvati_poteze(tabla)
        if potezi_topa:
            potezi.extend(potezi_topa)
        if potezi_lovca:
            potezi.extend(potezi_lovca)
        return potezi

    def vrati_bodove(self):
        return 240
    



class Kralj(Figura):

    def dohvati_poteze(self, tabla):
        potezi = []
        potezi += self.dohvati_horizontalne_poteze(tabla)
        potezi += self.dohvati_vertikalne_poteze(tabla)
        return potezi

    def dohvati_vertikalne_poteze(self, tabla):
        potezi = []
        for op in [operator.add, operator.sub]:
            x = op(self.x, 1)
            if tabla.prazno_polje(x, self.y) or tabla.ima_protivnika(self, x, self.y):
                potezi.append((x, self.y))
            if tabla.prazno_polje(x, self.y + 1) or tabla.ima_protivnika(self, x, self.y + 1):
                potezi.append((x, self.y + 1))
            if tabla.prazno_polje(x, self.y - 1) or tabla.ima_protivnika(self, x, self.y - 1):
                potezi.append((x, self.y - 1))
        return potezi

    def dohvati_horizontalne_poteze(self, tabla):
        potezi = []
        for op in [operator.add, operator.sub]:
            y = op(self.y, 1)
            if tabla.prazno_polje(self.x, y) or tabla.ima_protivnika(self, self.x, y):
                potezi.append((self.x, y))
        return potezi

    def vrati_bodove(self):
        return 1000