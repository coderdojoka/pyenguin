from pyenguin import *

__author__ = 'Mark Weinreuter'

fenster = Fenster(600, 480)
# Das Fenster ist die Standard-Szene
# Wir können weitere Szenen ganz einfach erstellen
s_links = Szene(200, 300, farbe=GRUEN)
s_rechts = Szene(100, 300, farbe=ROT)
s_rechts.x = 300

# Gegenstände werden standardmäßig zur Fenster-Szene hinzugefügt!
o = Oval(0, 0, 20, 20, BLAU)
p = Vieleck([(10, 10), (15, 20), (20, 10)], GRAU)

# Wir müssen sie von Hand in die korrekten Szenen einfügen
o.wechsle_szene(s_links)
p.wechsle_szene(s_rechts)




# Jede Szene hat ihre EIGENEN Maus-Ereignisse!!

def links_geklickt(x, y, ereignis):
    print("Klick links!")


def rechts_geklickt(x, y, ereignis):
    print("Klick rechts!")


s_rechts.registriere_maus_geklickt(rechts_geklickt)
s_links.registriere_maus_geklickt(links_geklickt)

s_links.registriere_maus_bewegt(lambda x, y, e: o.setze_position(x, y))
s_rechts.registriere_maus_bewegt(lambda x, y, e: p.setze_position(x, y))

fenster.starten()
