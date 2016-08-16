from pyenguin import *

__author__ = 'Mark Weinreuter'

fenster = Fenster(600, 480)
# Das Fenster ist die Standard-Szene
# Wir können weitere Szenen ganz einfach erstellen
g1 = Gruppe()
g2 = Gruppe()
g2.x = 100
g1.y = 300
g2.bewegung_x = .01
# Gegenstände werden standardmäßig zur Fenster-Szene hinzugefügt!
o = Oval(0, 0, 20, 20, BLAU)
p = Vieleck([(10, 10), (15, 20), (20, 10)], GRAU)
r = Rechteck(0, 0, 20, 20, ROT)
o.oben = 20

# Wir müssen sie von Hand in die Gruppen einfügen
o.wechsle_gruppe(g1)
r.wechsle_gruppe(g2)
p.wechsle_gruppe(g2)


# Jede Szene hat ihre EIGENEN Maus-Ereignisse!!

def links_geklickt(x, y, ereignis):
    print("Klick links!")


def rechts_geklickt(x, y, ereignis):
    print("Klick rechts!")


def aktualisiere(dt):
    if r.ist_raus():
        g2.bewegung_x *= -1


registriere_aktualisiere(aktualisiere)
fenster.starten()
