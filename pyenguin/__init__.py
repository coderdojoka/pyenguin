from pyenguin.cursor import MausZeiger
from pyenguin.dinge import Gruppe, Warte, Aktualisierbar
from pyenguin.ereignis import EreignisBearbeiter
from pyenguin.farben import *
from pyenguin.fenster import Fenster
from pyenguin.objekte import Flaeche, Text
from pyenguin.schrift import *
from pyenguin.sound import HintergrundMusik
from pyenguin.speicher import BildSpeicher, SoundSpeicher
from pyenguin.szene import Szene
from pyenguin.bild import BildAnimation, Bild, generiere_namen_liste
from pyenguin.tasten import *
from pyenguin.figur import Figur
from pyenguin.paket import *

__author__ = 'Mark Weinreuter'


def Rechteck(x, y, breite, hoehe, farbe, dicke=0):
    f = Flaeche(breite, hoehe, transparent=False)
    f.rechteck(0, 0, breite, hoehe, farbe, dicke=dicke)
    f.links = x
    f.oben = y

    return f


def Kreis(x, y, radius, farbe, dicke=0):
    f = Flaeche(radius * 2, radius * 2, transparent=True)
    f.kreis(0, 0, radius, farbe, dicke)
    f.setze_position(x, y)

    return f


def Oval(x, y, radius1, radius2, farbe, dicke=0):
    f = Flaeche(radius1 * 2, radius2 * 2, transparent=True)
    f.oval(0, 0, radius1, radius2, farbe, dicke)
    f.setze_position(x, y)

    return f


def Vieleck(punkte, farbe, dicke=0):
    xs = list(map(lambda p: p[0], punkte))
    ys = list(map(lambda p: p[1], punkte))
    minx = min(xs)
    miny = min(ys)
    punkte = [(x - minx, y - miny) for x, y in punkte]
    f = Flaeche(max(xs) - minx, max(ys) - miny, transparent=True)
    f.vieleck(punkte, farbe, dicke)
    f.links = minx
    f.oben = miny

    return f


def Linie(px, py, qx, qy, farbe, dicke=0):
    minx = min(px, qx)
    miny = min(py, qy)
    maxx = max(px, qx) - minx
    maxy = max(py, qy) - miny
    f = Flaeche(maxx, maxy, transparent=True)
    f.linie(0, 0, maxx, maxy, farbe, dicke)
    f.setze_position(minx, miny)
    return f


def registriere_alle_tasten(funktion):
    """
    Die Funktion wird aufgerufen, wenn eine beliebige Taste gedrückt wird

    :param funktion:
    :type funktion: (bool, str, int) -> None
    """
    Szene.aktive_szene.registriere_alle_tasten(funktion)


def entferne_alle_tasten(funktion):
    """
    Entfernt die Funktion wird aufgerufen, wenn eine beliebige Taste gedrückt wird

    :param funktion:
    :type funktion: (bool, Str, int) -> None
    """
    Szene.aktive_szene.entferne_alle_tasten(funktion)


def registriere_taste_oben(taste, funktion):
    """
    Registriert eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt und losgelassen wird.

    :param taste: die Taste z.B. die a-Taste ist 97. Die wichtigsten Tasten sind vordefiniert, so entspricht T_a der 'a'-Taste
    :type taste: int
    :param funktion: Die Funktion die aufgerufen wird. Sie muss 2 Parameter akzeptieren, der
    Erste gibt an, ob die Taste gedrückt oder losgelassen ist und der Zweite ist das Event Objekt
    :type funktion: (bool, pyenguin.Taste) -> None
    """
    Szene.aktive_szene.registriere_taste_oben(taste, funktion)


def entferne_taste_oben(taste, funktion):
    """
    Entfernt eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt und losgelassen wird.

    :param taste: die Taste
    :type taste: int
    :param funktion: Die Funktion die aufgerufen wird.
    :type funktion: (Taste) -> None
    """
    Szene.aktive_szene.entferne_taste_oben(taste, funktion)


def registriere_taste_unten(taste, funktion):
    """
    Registriert eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt wird.

    :param taste: die Taste z.B. die a-Taste ist 97. Die wichtigsten Tasten sind vordefiniert, so entspricht T_a der 'a'-Taste
    :type taste: int
    :param funktion: Die Funktion die aufgerufen wird. Sie muss 1 Parameter akzeptieren
    :type funktion: (Zeichen) -> None
    """
    Szene.aktive_szene.registriere_taste_unten(taste, funktion)


def entferne_taste_unten(taste, funktion):
    """
    Entfernt eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt wird.

    :param taste: die Taste
    :type taste: int
    :param funktion: Die Funktion die aufgerufen wird.
    :type funktion: (Taste) -> None
    """
    Szene.aktive_szene.entferne_taste_unten(taste, funktion)


def registriere_maus_bewegt(funktion):
    """
    Registriert eine Funktion, die ausgeführt wird, wenn eine Maus-Taste gedrückt wird.
    Wenn die Funktion aufgerufen wird, wird ihr ein Objekt übergeben, das so aufgebaut ist:

        button: 1-3 # welche Taste: 1 = Links, ...
        pos: (x,y) # Tupel mit der Position

    :param funktion: Die Funktion die aufgerufen werden soll, wenn eine Taste gedrückt wurde
    :type funktion: (object) -> None
    """
    Szene.aktive_szene.registriere_maus_bewegt(funktion)


def entferne_maus_bewegt(funktion):
    """
    Enfternt eine Funktion, die ausgeführt wird, wenn eine Maus-Taste gedrückt wird.
    Wenn die Funktion aufgerufen wird, wird ihr ein Objekt übergeben, das so aufgebaut ist:

        button: 1-3 # welche Taste: 1 = Links, ...
        pos: (x,y) # Tupel mit der Position

    :param funktion: Die Funktion die aufgerufen werden soll, wenn eine Taste gedrückt wurde
    :type funktion: (object) -> None
    """
    Szene.aktive_szene.registriere_maus_bewegt(funktion)


def registriere_maus_losgelassen(funktion):
    """
    Registriert eine Funktion, die aufgerufen wird, wenn eine Maustaste losgelassen wird.

    :param funktion: Die Funktion
    :type funktion: (object)->None
    """
    Szene.aktive_szene.registriere_maus_losgelassen(funktion)


def entferene_maus_losgelassen(funktion):
    """
    Entfernt eine Funktion, die aufgerufen wird, wenn eine Maustaste losgelassen wird.

    :param funktion: Die Funktion
    :type funktion: (object)->None
    """
    Szene.aktive_szene.entferene_maus_losgelassen(funktion)


def registriere_maus_geklickt(funktion):
    """
    Registriert eine Funktion, die aufgerufen wird, wenn eine Maustaste gedrückt wird.

    :param funktion:
    :type funktion: (object)->None
    """
    Szene.aktive_szene.registriere_maus_geklickt(funktion)


def entferne_maus_geklickt(funktion):
    """
    Entfernt eine Funktion, die aufgerufen wird, wenn eine Maustaste gedrückt wird.

    :param funktion:
    :type funktion: (object)->None
    """
    Szene.aktive_szene.entferne_maus_geklickt(funktion)


__HANDLER_NAMEN = list(filter(lambda s: s.find("registriere_") > -1 or s.find("entferne_") > -1, globals().keys()))

__all__ = [ "Bild", "BildAnimation", "generiere_namen_liste",
    "BildSpeicher", "SoundSpeicher", "Figur", "Szene", "Fenster", "Flaeche", "Gruppe",
    "EreignisBearbeiter", "Schrift", "Text", "Rechteck", "Kreis", "Oval", "Vieleck",
    "MausZeiger", "HintergrundMusik", "Warte", "Aktualisierbar"]

__all__.extend(FARBEN_NAMEN)
__all__.extend(TASTEN_NAMEN)
__all__.extend(__HANDLER_NAMEN)
__all__.extend(PAKET_NAMEN)
