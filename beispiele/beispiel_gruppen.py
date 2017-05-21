from pyenguin import *

__author__ = 'Mark Weinreuter'

fenster = Fenster(600, 480)
# Das Fenster ist die Standard-Szene
# Wir können weitere Szenen ganz einfach erstellen
g1 = Gruppe()
g2 = Gruppe()
g2.x = 100
g1.y = 300
#g2.bewegung_x = .01
# Gegenstände werden standardmäßig zur Fenster-Szene hinzugefügt!
o = Oval(0, 0, 40, 20, BLAU)
p = Vieleck([(0, 0), (30, 60), (60, 0)], ROT)
r = Rechteck(0, 0, 20, 20, ROT)
p.x = 200
k = Kreis(0,0,200,GRUEN,dicke=2)
# Wir müssen sie von Hand in die Gruppen einfügen
o.wechsle_gruppe(g2)
#r.wechsle_gruppe(g2)
p.wechsle_gruppe(g2)
k.wechsle_gruppe(g2)

# Jede Szene hat ihre EIGENEN Maus-Ereignisse!!

def links_geklickt(x, y, ereignis):
    print("Klick links!")


def rechts_geklickt(x, y, ereignis):
    print("Klick rechts!")
g2.zentriere()
winkel = 0
def aktualisiere(dt):
    #if r.ist_raus():
    #    g2.bewegung_x *= -1

    global winkel
    #winkel +=
    g2.rotiere(dt * .01)


registriere_aktualisiere(aktualisiere)
fenster.starten()
