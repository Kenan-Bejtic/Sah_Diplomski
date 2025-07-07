from Figura import *
from copy import deepcopy

class Tabla:

    bijeli_figure = []
    crne_figure = []

    def __init__(self, nacin_igre, ai=False, dubina=2, log=False):    # nacin_igre == 0 : bijeli dole / crni gore
        self.tabla = []
        self.nacin_igre = nacin_igre
        self.dubina = dubina
        self.ai = ai
        self.log = log

    def inicijaliziraj_tablu(self):
        for i in range(8):
            self.tabla.append(['prazno-polje' for _ in range(8)])

    def postavi_figure(self):
        self.tabla.clear()
        self.bijeli_figure.clear()
        self.crne_figure.clear()
        self.inicijaliziraj_tablu()
        self.kralj_bijeli = Kralj('bijeli', 0, 4, '\u265A')
        self.kralj_crni = Kralj('crni', 7, 4, '\u2654')
        for j in range(8):
            self[1][j] = Pijun('bijeli', 1, j, '\u265F')
            self[6][j] = Pijun('crni', 6, j, '\u2659')
        self[0][0] = Top('bijeli', 0, 0, '\u265C')
        self[0][7] = Top('bijeli', 0, 7, '\u265C')
        self[0][1] = Konj('bijeli', 0, 1, '\u265E')
        self[0][6] = Konj('bijeli', 0, 6, '\u265E')
        self[0][2] = Lovac('bijeli', 0, 2, '\u265D')
        self[0][5] = Lovac('bijeli', 0, 5, '\u265D')
        self[0][3] = Kraljica('bijeli', 0, 3, '\u265B')
        self[0][4] = self.kralj_bijeli
        self[7][0] = Top('crni', 7, 0, '\u2656')
        self[7][7] = Top('crni', 7, 7, '\u2656')
        self[7][1] = Konj('crni', 7, 1, '\u2658')
        self[7][6] = Konj('crni', 7, 6, '\u2658')
        self[7][2] = Lovac('crni', 7, 2, '\u2657')
        self[7][5] = Lovac('crni', 7, 5, '\u2657')
        self[7][3] = Kraljica('crni', 7, 3, '\u2655')
        self[7][4] = self.kralj_crni

        self.spasi_figure()

        if self.nacin_igre != 0:
            self.preokreni()

    def spasi_figure(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], Figura):
                    if self[i][j].boja == 'bijeli':
                        self.bijeli_figure.append(self[i][j])
                    else:
                        self.crne_figure.append(self[i][j])

    def izvrši_potez(self, figura, x, y, zadrži_povijest=False):    # Povijest se čuva pri pretraživanju poteza (AI)
        stari_x = figura.x
        stari_y = figura.y
        if zadrži_povijest:
            self.tabla[stari_x][stari_y].postavi_posljednju_pojedenu(self.tabla[x][y])
        else:
            if isinstance(self.tabla[x][y], Figura):
                if self.tabla[x][y].boja == 'bijeli':
                    self.bijeli_figure.remove(self.tabla[x][y])
                else:
                    self.crne_figure.remove(self.tabla[x][y])
        self.tabla[x][y] = self.tabla[stari_x][stari_y]
        self.tabla[stari_x][stari_y] = 'prazno-polje'
        self.tabla[x][y].postavi_poziciju(x, y, zadrži_povijest)

    def poništi_potez(self, figura):
        x = figura.x
        y = figura.y
        self.tabla[x][y].vrati_starupoziciju()
        stari_x = figura.x
        stari_y = figura.y
        self.tabla[stari_x][stari_y] = self.tabla[x][y]
        self.tabla[x][y] = figura.dohvati_posljednju_pojedenu()

    def preokreni(self):
        self.tabla = self.tabla[::-1]
        for i in range(8):
            for j in range(8):
                if isinstance(self.tabla[i][j], Figura):
                    fig = self.tabla[i][j]
                    fig.x = i
                    fig.y = j

    def __getitem__(self, item):
        return self.tabla[item]

    def ima_protivnika(self, figura, x, y):
        if not self.je_validan_potez(x, y):
            return False
        if isinstance(self.tabla[x][y], Figura):
            return figura.boja != self[x][y].boja
        return False

    def ima_prijatelja(self, figura, x, y):
        if not self.je_validan_potez(x, y):
            return False
        if isinstance(self[x][y], Figura):
            return figura.boja == self[x][y].boja
        return False

    @staticmethod
    def je_validan_potez(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def prazno_polje(self, x, y):
        if not self.je_validan_potez(x, y):
            return False
        return not isinstance(self[x][y], Figura)

    def dohvati_boju_igraca(self):
        if self.nacin_igre == 0:
            return 'bijeli'
        return 'crni'

    def kralj_je_ugrožen(self, boja, potez=None):
        if boja == 'bijeli':
            neprijatelji = self.crne_figure
            kralj = self.kralj_bijeli
        else:
            neprijatelji = self.bijeli_figure
            kralj = self.kralj_crni
        prijetnje = []
        for neprijatelj in neprijatelji:
            potezi = neprijatelj.dohvati_poteze(self)
            if (kralj.x, kralj.y) in potezi:
                prijetnje.append(neprijatelj)
        if potez and len(prijetnje) == 1 and prijetnje[0].x == potez[0] and prijetnje[0].y == potez[1]:
            return False
        return True if len(prijetnje) > 0 else False

    def zavrsena_igra(self):
        terminal1 = self.bijeli_pobjedio()
        terminal2 = self.crni_pobjedio()
        terminal3 = self.nerješeno()
        return terminal1 or terminal2 or terminal3

    def nerješeno(self):
        if not self.kralj_je_ugrožen('bijeli') and not self.ima_poteze('bijeli'):
            return True
        if not self.kralj_je_ugrožen('crni') and not self.ima_poteze('crni'):
            return True
        if self.nedovoljno_materijala():
            return True
        return False

    def bijeli_pobjedio(self):
        if self.kralj_je_ugrožen('crni') and not self.ima_poteze('crni'):
            return True
        return False

    def crni_pobjedio(self):
        if self.kralj_je_ugrožen('bijeli') and not self.ima_poteze('bijeli'):
            return True
        return False

    def ima_poteze(self, boja):
        ukupno_poteza = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], Figura) and self[i][j].boja == boja:
                    fig = self[i][j]
                    ukupno_poteza += len(fig.filtriraj_poteze(fig.dohvati_poteze(self), self))
                    if ukupno_poteza > 0:
                        return True
        return False

    def nedovoljno_materijala(self):
        ukupno_bijelih_konja = 0
        ukupno_crnih_konja = 0
        ukupno_bijelih_lovaca = 0
        ukupno_crnih_lovaca = 0
        ukupno_ostalih_bijelih_figura = 0
        ukupno_ostalih_crnih_figura = 0

        for fig in self.bijeli_figure:
            if fig.tip == 'Konj':
                ukupno_bijelih_konja += 1
            elif fig.tip == 'Lovac':
                ukupno_bijelih_lovaca += 1
            elif fig.tip != 'Kralj':
                ukupno_ostalih_bijelih_figura += 1

        for fig in self.crne_figure:
            if fig.tip == 'Konj':
                ukupno_crnih_konja += 1
            elif fig.tip == 'Lovac':
                ukupno_crnih_lovaca += 1
            elif fig.tip != 'Kralj':
                ukupno_ostalih_crnih_figura += 1

        slabe_bijele_figure = ukupno_bijelih_lovaca + ukupno_bijelih_konja
        slabe_crne_figure = ukupno_crnih_lovaca + ukupno_crnih_konja

        if self.kralj_bijeli and self.kralj_crni:
            if slabe_bijele_figure + ukupno_ostalih_bijelih_figura + slabe_crne_figure + ukupno_ostalih_crnih_figura == 0:
                return True
            if slabe_bijele_figure + ukupno_ostalih_bijelih_figura == 0:
                if slabe_crne_figure == 1:
                    return True
            if slabe_crne_figure + ukupno_ostalih_crnih_figura == 0:
                if slabe_bijele_figure == 1:
                    return True
            if len(self.bijeli_figure) == 1 and len(self.crne_figure) == 16 or len(self.crne_figure) == 1 and len(self.bijeli_figure) == 16:
                return True
            if ukupno_bijelih_konja == slabe_bijele_figure + ukupno_ostalih_bijelih_figura and len(self.crne_figure) == 1:
                return True
            if ukupno_crnih_konja == slabe_crne_figure + ukupno_ostalih_crnih_figura and len(self.bijeli_figure) == 1:
                return True
            if slabe_bijele_figure == slabe_crne_figure == 1 and ukupno_ostalih_bijelih_figura == ukupno_ostalih_crnih_figura == 0:
                return True

    def procijeni(self):
        bodovi_bijelih = 0
        bodovi_crnih = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], Figura):
                    fig = self[i][j]
                    if fig.boja == 'bijeli':
                        bodovi_bijelih += fig.vrati_bodove()
                    else:
                        bodovi_crnih += fig.vrati_bodove()
        if self.nacin_igre == 0:
            return bodovi_crnih - bodovi_bijelih
        return bodovi_bijelih - bodovi_crnih

    def __str__(self):
        return str(self[::-1]).replace('], ', ']\n')

    def __repr__(self):
        return 'Tabla'

    def prikaz_unicode_niza(self):
        podaci = deepcopy(self.tabla)
        for idx, red in enumerate(self.tabla):
            for i, p in enumerate(red):
                if isinstance(p, Figura):
                    un = p.unicode
                else:
                    un = '\u25AF'
                podaci[idx][i] = un
        return podaci[::-1]

    def dohvati_kralja(self, figura):
        if figura.boja == 'bijeli':
            return self.kralj_bijeli
        return self.kralj_crni