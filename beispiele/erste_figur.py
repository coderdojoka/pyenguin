from pyenguin import *

__author__ = 'Mark Weinreuter'

# Fenster mit Größe und Titel
fenster = Fenster(640, 480, "Hallo Fenster")

# Es kommen viele Bilder bereits mit.
# Lade eine Bild in den BildSpeicher und gib im einen Namen
BildSpeicher.lade_aus_paket("blocky", "spieler/p1_stand.png")

# Figur erstellen. Gib hier den Bildnamen im Speicher an
figur = Figur("blocky")

# Das Fenster starten
fenster.starten()
