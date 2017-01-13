# Importiert alle wichtigen pyenguin Befehle
from pyenguin import *

__author__ = 'Mark Weinreuter'

# Fenster mit Größe und Titel erstellen
fenster = Fenster(400, 200, "Hallo Bilder")

# Ein Bild zur Verwendung hinzufügen (einmal machen): Name, Dateipfad
BildSpeicher.lade("planet", "test_bild.png")
BildSpeicher.lade("mond", "test_bild2.png")

# Das Bild anzeigen. Über den Namen wird es wiedergefunden
bild1 = BildSpeicher.gib("planet")
bild1.abstand_links = 40
bild1.abstand_oben = 50

# Das Bild nochmals anzeigen.
bild2 = BildSpeicher.gib("planet")
bild2.abstand_rechts = 40
bild2.abstand_unten = 50

# Zweites Bild anzeigen
bild3 = BildSpeicher.gib("mond")
bild3.links = bild1.rechts + 10
bild3.oben = bild1.oben + 10

# Zweites Bild nochmal anzeigen
bild4 = BildSpeicher.gib("mond")
bild4.links = bild2.rechts + 10
bild4.unten = bild2.unten + 10

# Das Fenster anzeigen
fenster.starten()
