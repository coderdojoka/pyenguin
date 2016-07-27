import random

from pyenguin import *

# Der erste Schritt, um ein fenster zu starten ist immer init() aufzurufen
fenster = Fenster(640, 480, "Klicke auf das Haus!")
# Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein fenster"


# Ein Quadrat an der Position 300x200
haus = Rechteck(300, 200, 100, 100, GELB)

# Ein Dreieck zeichenn, in dem alle Eckpunte angegeben werden
dreieck = Vieleck([(300, 200), (350, 160), (400, 200)], ROT)

# Ein weiteres Quadrat
box = Rechteck(100, 100, 50, 50, GRUEN)


# Wird aufgerufen, immer wenn die Maus bewegt wird
def maus_bewegt(x, y, ereignis):
    maus_position = ereignis.pos
    print(maus_position)


def zeit_abgelaufen():
    print("Wartezeit ist abgelaufen")


def zeit_wieder_abgelaufen():
    print("Wartezeit ist schon wieder abgelaufen")


def wenn_beendet():
    print("Fenster wird geschloßen.")


fenster.registriere_wird_beendet(wenn_beendet)


# In 1000 ms = 1s wird die Funktion zeit_abgelaufen ausgeführt
# Warte(1000, zeit_abgelaufen)
# Alle 1000ms wird die Funktion zeit_wieder_abgelaufen ausgeführt
# Warte(1000, zeit_wieder_abgelaufen, True)


# Wird aufgerufen, immer wenn die Maus gedrueckt (geklickt) wird
def maus_gedrueckt(x, y, ereignis):
    maus_position = (x, y)
    print(ereignis.button)
    # Maus-Button Nummern:
    # 1: Links
    # 2: Mitte (Mausrad)
    # 3: Rechts
    # Diese Nummern habe ich auf meinem Laptop mit Touchpad bekommen
    # 4: Scroll hoch
    # 5: Scroll runter
    # 6: Scroll rechts
    # 7: Scroll links

    if ereignis.button != 1:
        return

    if box.punkt_innerhalb(maus_position):
        box.farbe = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    if dreieck.punkt_innerhalb(maus_position):
        dreieck.setze_position(random.randint(10, 500), random.randint(10, 455))

    if haus.punkt_innerhalb(maus_position):
        haus.setze_position(random.randint(10, 500), random.randint(10, 455))


# Bindet die Funktion 'maus_gedrueckt' an das maus_gedrueckt-Ereignis
registriere_maus_geklickt(maus_gedrueckt)

# Bindet die Funktion 'maus_bewegt' an das maus_bewegt-Ereignis
registriere_maus_bewegt(maus_bewegt)

dreieck.setze_bei_maus_klick(lambda x, y, e: dreieck.entferene())

# Hilfsgitter einblenden
fenster.zeichne_gitter()

# Um das fenster zu starten, muss fenster.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
fenster.starten()
