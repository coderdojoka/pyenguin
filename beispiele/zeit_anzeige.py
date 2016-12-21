import datetime

from pyenguin import *

__author__ = 'Mark Weinreuter'

fenster = Fenster(640, 480, "Aktuelle Uhrzeit")

text = Text("", Schrift(20))
text.zentriere()


def aktualisiere(dt):
    # aktuelle Uhrzeit + Datum
    jetzt = str(datetime.datetime.now())
    text.setze_text(jetzt)


registriere_aktualisiere(aktualisiere)

fenster.starten()
