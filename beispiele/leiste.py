__author__ = 'Mark Weinreuter'

from pyenguin import *

fenster = Fenster()

w = 16
h = 14 * 30
steps = 14
off = h / steps

dicke = 2

f = Flaeche(w, h + dicke, transparent=True)
#f.fuelle(GRUEN)

f.linie(w // 2-1, 0, w // 2-1, h, DUNKEL_GRAU)
f.linie(w // 2, 0, w // 2, h, GRAU)

Warte(100, lambda: f.als_bild_speichern("test.png"))

for i in range(0, steps + 1):
    y = i * off
    f.linie(0, y, w, y, GRAU, dicke=dicke)
    f.linie(0, y, w, y, DUNKEL_GRAU, dicke=1)

fenster.starten()
