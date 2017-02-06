from pyenguin import *

__author__ = 'Mark Weinreuter'

# Fenster mit Größe und Titel
fenster = Fenster(640, 480, "Hallo Fenster")

# Generiere eine Liste von Namen. %02d wird durch die Zahlen: 01 ... 11 ersetzt
namen_liste = generiere_namen_liste("spieler/p1_gehen/p1_%02d.png", 1, 11)
# Lade alle Bilder auf einmal. Die Bilder kommen mit pyenguin mit!
# => lade_aus_paket
schluessel = BildSpeicher.lade_aus_paket("blocky", namen_liste)

# Figur erstellen. Gib hier den Bildnamen im Speicher an
BildSpeicher.lade_aus_paket("stehen", SPIELER_S1_STEHEN)
b1 = Bild("stehen")

Szene.aktive_szene.farbe = BLAU
b = BildAnimation(schluessel, wiederhole=True, skalierung=.8)
b.start()

f = Figur(b)
f.neue_kostueme(b1)
f.zentriere()

f.naechstes()


def test(x, y, e):
    f.naechstes()
    print(f.dimension())


f.setze_bei_maus_klick(test)

# Das Fenster starten
fenster.starten()
