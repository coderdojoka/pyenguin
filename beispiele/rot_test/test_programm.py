from pyenguin import *

fenster = Fenster(200, 200)

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

test.setze_rotation(45)
print(test.dimension())
test.als_bild_speichern("test_bild_45_aa.png")

test.skaliere(2)
print(test.dimension())
test.als_bild_speichern("test_bild_45_x2_aa.png")

fenster.starten()
