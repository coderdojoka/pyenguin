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


# Wird aufgerufen, immer wenn die Maus gedrueckt (geklickt) wird
def maus_gedrueckt(x, y, ereignis):
    maus_position = (x, y)

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

# Hilfsgitter einblenden
fenster.zeichne_gitter()

# Um das fenster zu starten, muss fenster.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
fenster.starten()
