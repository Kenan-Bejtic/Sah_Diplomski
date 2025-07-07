import Grafika
from Tabla import *

if __name__ == '__main__':
    nastavi_igrati = True

    tabla = Tabla(nacin_igre=0, ai=True, dubina=3, log=True) 

    while nastavi_igrati:
        Grafika.inicijaliziraj()
        tabla.postavi_figure()
        Grafika.nacrtaj_pozadinu(tabla)
        nastavi_igrati = Grafika.pokreni(tabla)
