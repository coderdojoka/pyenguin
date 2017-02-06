from pyenguin import *

__author__ = 'Mark Weinreuter'

# Fenster mit Größe und Titel
fenster = Fenster(640, 480, "Hallo Fenster")

# Es kommen viele Bilder bereits mit.
# Lade eine Bild in den BildSpeicher und gib im einen Namen
namen_liste = generiere_namen_liste("spieler/p1_gehen/p1_%02d.png", 1, 11)
schluessel = BildSpeicher.lade_aus_paket("blocky", namen_liste)

# Figur erstellen. Gib hier den Bildnamen im Speicher an
# figur.wechsle_bilder()
# figur.wechsle_bilder([0, 1])
BildSpeicher.lade_aus_paket("stehen", SPIELER_S1_STEHEN)
b1 = Bild("stehen")
b1.oben = 50

Szene.aktive_szene.farbe = BLAU
b = BildAnimation(schluessel, wiederhole=True, skalierung=.8)
print("Größe", b.width, b.height)
b.start()

f = Figur(b)
f.neue_kostueme(b1)
f.zentriere()

f.naechstes()
f.naechstes()


def test(x, y, e):
    f.naechstes()
    print(f.dimension())


f.setze_bei_maus_klick(test)

# Das Fenster starten
fenster.starten()
