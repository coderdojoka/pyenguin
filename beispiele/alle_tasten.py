__author__ = 'Mark Weinreuter'

from pyenguin import *

fenster = Fenster()


def alle(unten, taste, ereignis):
    print("Taste: ", taste, " ist gerade unten:", unten)


registriere_alle_tasten(alle)

fenster.starten()
