from pyenguin import *

__author__ = 'Mark Weinreuter'

ball_x = .3
ball_y = .1
speed = .1


def aktualisiere(dt):
    global ball_x, ball_y

    # Überprüfen ob der Ball die Kanten berührt
    if ball.ist_rechts_raus():
        ball_x *= -1
    elif ball.raus_links():
        ball_x *= -1

    if ball.ist_obenunten_raus():
        ball_y *= -1

    # Ball bewegen
    ball.aendere_position(ball_x * dt, ball_y * dt)

    # Kollision der zwei Rechtecke überprüfen
    beruehrt = rechteck.box_beruehrt(kollision)
    if beruehrt:
        kollision.farbe = ROT
    else:
        kollision.farbe = GELB


# Diese Funktionen werden aufgerufen, wenn die entsprechende Taste gedrückt wird
def links(taste):
    rechteck.bewegung_x = -speed


def links_oben(taste):
    rechteck.bewegung_x = 0


def rechts(taste):
    rechteck.bewegung_x = speed


def oben(taste):
    rechteck.bewegung_y = -speed


def unten(dt):
    rechteck.bewegung_y = speed


# Initialisiert das Fenster
fenster = Fenster(400, 400, "Steuere das blaue Rechteck!")

# Zwei Rechtecke erstellen
rechteck = Rechteck(40, 160, 40, 40, BLAU)
kollision = Rechteck(50, 40, 60, 40, ROT)

# Einen Text anzeigen
schrift = Schrift(20)
t = Text("Pfeiltasten zum bewegen", schrift, GRAU)

# 5 Pixel vom rechten Rand plazieren
t.abstand_links = 5
t.abstand_unten = 20
print(t.abstand_unten, t.abstand_links, t.abstand_rechts, t.abstand_oben)

# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_aus_paket("block", "gegner/blocker.png")
# Bild aus dem Speicher über seinen Schlüssel holen
ball = BildSpeicher.gib("block")
ball.x = 200
ball.y = 200

# Tastendrücke-Funktionen registrien. Wird die Taste T_a = 'a' gedrückt, so wird die
# Funktion mit dem Namen links aufgerufen
registriere_taste_unten(T_LINKS, links)
registriere_taste_unten(T_RECHTS, rechts)
registriere_taste_unten(T_UNTEN, unten)
registriere_taste_unten(T_OBEN, oben)

registriere_taste_oben(T_LINKS, links_oben)
registriere_taste_oben(T_RECHTS, links_oben)

rechteck.nach_vorne()
def zeit_um():
    rechteck.rotiere(5)
    print(rechteck)

Warte(100, zeit_um, True)

registriere_aktualisiere(aktualisiere)

# Das fenster starten
fenster.starten()
