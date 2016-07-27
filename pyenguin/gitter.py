from pyenguin.farben import *
from pyenguin.szene import Szene

__author__ = 'Mark Weinreuter'


class Gitter(Szene):
    def __init__(self, breite, hoehe, groesse=50, zahlen=True):
        """
        Zeichnet ein gitter mit der gegebenen Gittergröße.

        :param groesse: die Größe, Standart: 50
        :type groesse: int
        """

        Szene.__init__(self, breite, hoehe, transparent=True)

        # Anzahl an horizontalen Gitterlinien
        anzahl = round(breite / groesse)

        self.registriere_maus_geklickt(lambda a, b, c: print("kkk"))

        if zahlen:
            from pyenguin.flaeche import Schrift
            schrift = Schrift(20)

        for i in range(1, anzahl):
            self.flaeche.linie(i * groesse, 0, i * groesse, hoehe, HELL_GRAU)
            if zahlen:
                self.flaeche.text("%d" % (i * groesse), i * groesse, 2, schrift=schrift)

        # Anzahl an vertikalen Gitterlinien
        anzahl = round(hoehe / groesse)
        for i in range(1, anzahl):
            self.flaeche.linie(0, i * groesse, breite, i * groesse, HELL_GRAU)
            if zahlen:
                self.flaeche.text("%d" % (i * groesse), 2, i * groesse, schrift=schrift)
