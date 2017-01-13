# Importiert alle wichtigen pyenguin Befehle
from pyenguin import *

__author__ = 'Mark Weinreuter'

# Fenster mit Größe und Titel erstellen
fenster = Fenster(640, 480, "Hallo Fenster")

# Ein blaues Rechteck. Mitte bei: 200x100, Größe: 40x60
r = Rechteck(200, 100, 40, 60, BLAU)

# Das Fenster anzeigen
fenster.starten()
