__author__ = 'Mark Weinreuter'

from pyenguin import *

fenster = Fenster(600, 480)

# Eine Fläche an der Position (0|0)
block = Flaeche(200, 40)
block.fuelle(ROT)
punkt = Flaeche(20, 20)
punkt.kreis(0, 0, 10, BLAU)
g = Gruppe()

# Fläche in die Gruppe einfügen
block.wechsle_gruppe(g)
punkt.wechsle_gruppe(g)

# Gruppen position ändern
g.zentriere()


# => "Welt"-Position der Fläche = Position Gruppe + Position Fläche in Gruppe


def links_gruppe(e):
    g.aendere_position(-10, 0)


def links_punkt(e):
    punkt.aendere_position(-10, 0)


registriere_taste_unten(T_LINKS, links_gruppe)
registriere_taste_unten(T_a, links_punkt)

def klick(x,y,e):
    e.ding.fuelle(GELB)

punkt.setze_bei_maus_klick(klick)

fenster.starten()
