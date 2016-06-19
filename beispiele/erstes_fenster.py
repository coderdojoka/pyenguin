from pyenguin import *

__author__ = 'Mark Weinreuter'

# Fenster mit Größe und Titel
fenster = Fenster(640, 480, "Hallo Fenster")

# Ein blaues Rechteck. Mitte des Rechtecks: 200x100
r = Rechteck(200, 100, 240, 100, BLAU)
def test(x,y, ereignis):
    print("Test")
r.setze_bei_maus_klick(test)

# Das Fenster starten
fenster.starten()
