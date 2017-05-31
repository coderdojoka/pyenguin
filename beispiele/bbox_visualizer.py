from pyenguin.szene import SzenenListe

__author__ = 'Mark Weinreuter'

from pyenguin import *


def zeichne_bboxen():
    fl.fuelle(WEISS)

    def zeichne_kind_boxen(elter):
        for ding in elter.kind_dinge:

            if ding == fl:  # die fläche auf die wir zeichnen überspringen
                continue

            fl.rechteck(ding.welt_x - ding.breite / 2, ding.welt_y - ding.hoehe / 2, ding.breite, ding.hoehe,
                        ding.farbe)
            # welt_x ist die Position in der Welt(Fenster), falls Elemente sich in Gruppen befinden!

            # Gruppen rekursiv zeichnen
            if isinstance(ding, Gruppe):
                zeichne_kind_boxen(ding)

    zeichne_kind_boxen(Szene.fenster_szene)


fenster = Fenster(titel="Leertaste drücken!")
fl = Flaeche(fenster.breite, fenster.hoehe)
fl.zentriere()

r1 = Rechteck(0, 0, 50, 250, BLAU)
k1 = Oval(0, 0, 70, 140, MATT_GOLD)
g1 = Gruppe()

k1.x = 50
r1.y = 100

k1.wechsle_gruppe(g1)
r1.wechsle_gruppe(g1)
g1.zentriere()

# neue farben eigenschaft, für die BBoxen
k1.farbe = GRAU_GOLD
r1.farbe = HELL_BLAU
g1.farbe = HELL_GRUEN


def aktualisiere(dt):
    if ist_unten:
        g1.rotiere(1)
        zeichne_bboxen()
        print(g1)
        print(r1)
        print(k1)


ist_unten = False


def t_unten(e):
    global ist_unten
    ist_unten = True


def t_oben(e):
    global ist_unten
    ist_unten = False


registriere_taste_oben(T_LEER, t_oben)
registriere_taste_unten(T_LEER, t_unten)
registriere_aktualisiere(aktualisiere)

fenster.starten()
