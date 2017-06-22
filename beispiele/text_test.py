from random import randint

from pyenguin import *

__author__ = 'Mark Weinreuter'

fenster = Fenster()
fbt = FesteBreiteText(200, Schrift(20), "Hallo Welt von Mark",hintergrund=GRUEN, min_hoehe=100)

fbt.zentriere()

Warte(2000, lambda : fbt.setze_text("Neuer Text, der viel länger ist" * randint(2,5)), True)

fenster.starten()