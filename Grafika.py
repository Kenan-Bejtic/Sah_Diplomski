# Modul grafika.py (prethodni graphics.py)
import pygame
from Figura import *
from Racunar import dohvati_slucajni_potez, dohvati_ai_potez

tamni_blok = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/square brown dark_png_shadow_128px.png')
svijetli_blok = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/square brown light_png_shadow_128px.png')
tamni_blok = pygame.transform.scale(tamni_blok, (75, 75))
svijetli_blok = pygame.transform.scale(svijetli_blok, (75, 75))

bijeliPijun = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_pawn_png_shadow_128px.png')
bijeliPijun = pygame.transform.scale(bijeliPijun, (75, 75))
bijeliTop = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_rook_png_shadow_128px.png')
bijeliTop = pygame.transform.scale(bijeliTop, (75, 75))
bijeliLovac = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_bishop_png_shadow_128px.png')
bijeliLovac = pygame.transform.scale(bijeliLovac, (75, 75))
bijeliKonj = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_knight_png_shadow_128px.png')
bijeliKonj = pygame.transform.scale(bijeliKonj, (75, 75))
bijeliKralj = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_king_png_shadow_128px.png')
bijeliKralj = pygame.transform.scale(bijeliKralj, (75, 75))
bijeliKraljica = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_queen_png_shadow_128px.png')
bijeliKraljica = pygame.transform.scale(bijeliKraljica, (75, 75))

crniPijun = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_pawn_png_shadow_128px.png')
crniPijun = pygame.transform.scale(crniPijun, (75, 75))
crniTop = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_rook_png_shadow_128px.png')
crniTop = pygame.transform.scale(crniTop, (75, 75))
crniLovac = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_bishop_png_shadow_128px.png')
crniLovac = pygame.transform.scale(crniLovac, (75, 75))
crniKonj = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_knight_png_shadow_128px.png')
crniKonj = pygame.transform.scale(crniKonj, (75, 75))
crniKralj = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_king_png_shadow_128px.png')
crniKralj = pygame.transform.scale(crniKralj, (75, 75))
crniKraljica = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_queen_png_shadow_128px.png')
crniKraljica = pygame.transform.scale(crniKraljica, (75, 75))

istaknut_blok = pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/highlight_128px.png')
istaknut_blok = pygame.transform.scale(istaknut_blok, (75, 75))

ekran = None
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

def inicijaliziraj():
    global ekran
    pygame.init()
    pygame.display.set_caption('Šah!')
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    ekran = pygame.display.set_mode((600, 650))
    ekran.fill((0, 0, 0))

def nacrtaj_pozadinu(tabla):
    blok_x = 0
    for i in range(4):
        blok_y = 0
        for j in range(4):
            ekran.blit(svijetli_blok, (blok_x, blok_y))
            ekran.blit(tamni_blok, (blok_x + 75, blok_y))
            ekran.blit(svijetli_blok, (blok_x + 75, blok_y + 75))
            ekran.blit(tamni_blok, (blok_x, blok_y + 75))
            blok_y += 150
        blok_x += 150
    korak_x = 0
    korak_y = pygame.display.get_surface().get_size()[0] - 75
    for i in range(8):
        for j in range(8):
            if isinstance(tabla[i][j], Figura):
                obj = globals()[f'{tabla[i][j].boja}{tabla[i][j].tip}']
                ekran.blit(obj, (korak_x, korak_y))
            korak_x += 75
        korak_x = 0
        korak_y -= 75
    pygame.display.update()

def nacrtaj_tekst(tekst):
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    ekran.blit(s, (100, 600))
    tekst_surface = font.render(tekst, False, (237, 237, 237))
    if 'DRAW' in tekst:
        x = 260
    else:
        x = 230
    tekst_surface_restart = font.render('Pritisni "SPACE" za restart', False, (237, 237, 237))
    ekran.blit(tekst_surface, (x, 600))
    ekran.blit(tekst_surface_restart, (150, 620))
    pygame.display.update()

def pokreni(tabla):
    global ekran
    moguci_potezi_figura = []
    radi = True
    vidljivi_potezi = False
    dimenzije = pygame.display.get_surface().get_size()
    kraj_igre = False
    figura = None
    if tabla.nacin_igre == 1 and tabla.ai:
        dohvati_ai_potez(tabla)
        nacrtaj_pozadinu(tabla)
    while radi:
        if kraj_igre:
            nacrtaj_tekst(tekst_kraja_igre)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                radi = False
            if kraj_igre and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and not kraj_igre:
                x = 7 - pygame.mouse.get_pos()[1] // 75
                y = pygame.mouse.get_pos()[0] // 75
                if isinstance(tabla[x][y], Figura) and (tabla.dohvati_boju_igraca() == tabla[x][y].boja or not tabla.ai) and (x, y) not in moguci_potezi_figura:
                    figura = tabla[x][y]
                    potezi = figura.filtriraj_poteze(figura.dohvati_poteze(tabla), tabla)
                    pozicije_poteza = []
                    moguci_potezi_figura = []
                    for potez in potezi:
                        pozicije_poteza.append((dimenzije[0] - (8 - potez[1]) * 75, dimenzije[1] - potez[0] * 75 - 125))
                        potez_x = 7 - pozicije_poteza[-1][1] // 75
                        potez_y = pozicije_poteza[-1][0] // 75
                        moguci_potezi_figura.append((potez_x, potez_y))
                    if vidljivi_potezi:
                        nacrtaj_pozadinu(tabla)
                        vidljivi_potezi = False
                    for pozicija in pozicije_poteza:
                        vidljivi_potezi = True
                        ekran.blit(istaknut_blok, (pozicija[0], pozicija[1]))
                        pygame.display.update()
                else:
                    kliknuti_potez = (x, y)
                    try:
                        if kliknuti_potez in moguci_potezi_figura:
                            tabla.izvrši_potez(figura, x, y)
                            moguci_potezi_figura.clear()
                            nacrtaj_pozadinu(tabla)
                            if tabla.ai:
                                dohvati_ai_potez(tabla)
                                nacrtaj_pozadinu(tabla)
                                    
                        if tabla.bijeli_pobjedio():
                            kraj_igre = True
                            tekst_kraja_igre = 'BIJELI POBJEDIO!'
                        elif tabla.crni_pobjedio():
                            kraj_igre = True
                            tekst_kraja_igre = 'CRNI POBJEDIO!'
                        elif tabla.nerješeno():
                            kraj_igre = True
                            tekst_kraja_igre = 'NERJEŠENO!'
                    except UnboundLocalError:
                        pass
