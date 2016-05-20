from pyenguin import *

__author__ = 'Mark Weinreuter'

fenster = Fenster(600)

s = Szene(300, 300, farbe=GRUEN)
szene_rechts = Szene(300, 300, farbe=ROT)
szene_rechts.x = 300

o = Oval(0, 0, 10, 20, BLAU)
s.dazu(o)

p = Vieleck([(10, 10), (15, 20), (20, 10)], GRAU)
szene_rechts.dazu(p)

szene_rechts.registriere_maus_geklickt(lambda x, y, b: print(b))
s.registriere_maus_bewegt(lambda x, y, e: o.setze_position(x, y))
szene_rechts.registriere_maus_bewegt(lambda x, y, e: p.setze_position(x, y))

SoundSpeicher.lade_aus_paket("a", "a_ton.wav")
s = SoundSpeicher.gib("a")
s.setze_lautstaerke(.2)
s.play()
s.pause()

BildSpeicher.lade_aus_paket("snail", "gegner/blocker.png")
BildSpeicher.lade_aus_paket("snail2", "gegner/blocker_sauer.png")

BildSpeicher.lade_aus_paket("fliege", ["gegner/fliege_fliegen1.png", "gegner/fliege_fliegen2.png"])


f = Figur("snail")
f.neue_bilder("snail2")

f.wechsle_bilder = True
szene_rechts.dazu(f)
f.oben = 200
f.rechts = 200

f2 = Figur(["fliege_0", "fliege_1"])
f2.wechsle_bilder = True
f2.wechsel_dauer = 100
szene_rechts.dazu(f2)
f2.unten = 200
f2.links = 20

HintergrundMusik.lade_aus_paket("acdc.ogg")
HintergrundMusik.setze_lautstaerke(.2)
HintergrundMusik.start()
MausZeiger.neu("..", MausZeiger.cursor_m_strings)

w = Warte(3000, lambda : HintergrundMusik.pause())

fenster.starten()
