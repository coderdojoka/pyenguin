import pygame

__author__ = 'Mark Weinreuter'
from py2cd import *

aktuelles_fenster = Fenster()

f = Flaeche(40, 40, transparent=True)
f.kreis(0, 0, 20, (255, 0, 0))
r = Rechteck(100, 100, 50, 50, (0, 24, 55))
k = Kreis(30, 40, 20, (0, 255, 0))
o = Oval(300, 150, 30, 40, (0, 45, 22), 3)
g = Gruppe()


def test(dt):
    if f.ist_raus():
        print("aus")


BildSpeicher.lade_aus_paket("fliege", ["gegner/fliege_fliegen1.png", "gegner/fliege_fliegen2.png"])
BildSpeicher.lade_aus_paket("fliege_tot", ["gegner/fliege_tot.png"])

f.bild("fliege_tot", 10, 10)

af = Figur("fliege_0")
af.neue_bilder("fliege_1")

aktuelles_fenster.registriere_aktualisierung(test)
Szene.fenster_szene.registriere_maus_geklickt(lambda x, y, b: print(x, y, b))
Szene.fenster_szene.registriere_maus_bewegt(lambda x, y, e: af.setze_position(x, y))


def unten(a):
    print(a)
    af.naechstes_bild()


Szene.fenster_szene.registriere_taste_unten(pygame.constants.K_SPACE, unten)


BildSpeicher.liste_paket_bilder()

g.dazu(k)
g.dazu(f)
g.bewegung_y = 1
# f.bewegung_y = 1
f.bewegung_x = 2
t = Text("Hallo")
# t.bewegung_x = .5
# t.bewegung_y = .4
g.dazu(t)
aktuelles_fenster.zeichne_gitter()
aktuelles_fenster.starten()
