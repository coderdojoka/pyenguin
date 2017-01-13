from pyenguin import *

fenster = Fenster(400, 200)

BildSpeicher.lade("TEST", "Strasse_T-Kreuzung.png")
test = BildSpeicher.gib("TEST")
test.x = 100
test.y = 100
print(test.dimension())

#test.rotiere(90, False) # Schaltet Antialiasing aus
print(test.dimension())
test.als_bild_speichern("test_bild_normal.png")

#test.setze_rotation(90)  # Hier mit sezte, da 2mal rotiere ja 180° sind
print(test.dimension())
test.als_bild_speichern("test_bild_aa.png")

test.setze_rotation(45, False)
print(test.dimension())
test.als_bild_speichern("test_bild_45_normal.png")


# Zweites Bild anzeigen
test2 = BildSpeicher.gib("TEST")
test2.setze_rotation(45, True)
print(test2.dimension())
test2.als_bild_speichern("test_bild_45_aa.png")

# Zweites Bild rechts neben dem ersten Bild
test2.links = test.rechts + 10
test2.oben = test.oben


fenster.starten()
