import random

from gui_simulation import *
from pyenguin import *
from pyenguin.pygameui import *

__author__ = 'Mark Weinreuter'

mars_radius = 3389.5
phOrbit = 6000

phMass = 1.0659 * 10 ** 16

fw = 1000
sw = 1000
fh = sw
fenster = Fenster(fw, fh)

# 2 Szenen erstellen und anordnen
spielSzene = Szene(sw, fh, farbe=GRUEN)

# Lade_bilder
BildSpeicher.lade("planet", "bilder/planet.png")
BildSpeicher.lade("mond", "bilder/mond.png")
BildSpeicher.lade("rakete", "bilder/rakete.png")

# 3 Hauptfiguren
bplanet = BildSpeicher.gib("planet")
brakete = BildSpeicher.gib("rakete")
bmond = BildSpeicher.gib("mond")

# Größen errechnen/speichern
planet_radius = bplanet.breite / 2
mond_radius = bmond.breite / 2
rakete_radius = brakete.height / 2
abstand_mond = 120

# Positionen setzen
bplanet.zentriere()
brakete.setze_position(bplanet.x, bplanet.oben - rakete_radius)
bmond.setze_position(bplanet.x, bplanet.oben - abstand_mond)

mond = GMond(100000, (fh - 50) / 2, .02)

planet = GPlanet(100000)

simu = GSimulation(planet, mond)
for i in range(0, 100):
    f = random.randint(30, 80)
    a = random.randint(-40, 40)
    simu.neue_grakete(f, a)

# Zur Spielszene hinzufügen
spielSzene.dazu(simu.gruppe)

simu.gruppe.zentriere()


def aktualisiere(dt):
    simu.naechster_schritt()


fenster.registriere_aktualisierung(aktualisiere)
fenster.starten()
