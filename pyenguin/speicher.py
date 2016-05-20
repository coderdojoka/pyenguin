import pygame
from pyenguin.objekte import Flaeche

from pyenguin.helfer import *
from pyenguin.sound import Sound

__author__ = 'Mark Weinreuter'


class _Speicher:
    def __init__(self, resourcen_pfad, erlaubte_endungen):
        self.erlaubte_endungen = erlaubte_endungen
        self.speicher = {}
        self.resourcen_pfad = resourcen_pfad

    def lade_aus_paket(self, schluessel, pfade):
        ordner = kombiniere_pfad(ordner_pfad(), self.resourcen_pfad)
        self.lade(schluessel, pfade, ordner)

    def lade(self, schluessel, pfade, start_ordner=""):
        """

        :param schluessel:  Der Schlüssel oder einen Liste von Schlüssel
        :type schluessel: str|list[str]
        :param pfade: Der Pfad oder eine Liste von Pfaden
        :type pfade: str|list[str]
        :param alpha:
        :type alpha:
        :return:
        :rtype:
        """
        pus = pfade_und_schluessel(pfade, schluessel)

        for pfad, name in pus:
            pfad = kombiniere_pfad(start_ordner, pfad)
            print("Lade Sound:", name, pfad)

            s = self.neue_instanz(pfad)
            self.speicher[name] = s

    def gib(self, schluessel):
        if schluessel not in self.speicher:
            raise AttributeError("Der Eintrag %s ist nicht vorhanden. Du musst ihn zuerst laden." % schluessel)

        return self._gib_speicher_element(schluessel)

    def _gib_speicher_element(self, schluessel):
        return self.speicher[schluessel]

    def liste_im_paket(self):
        """
        Listet alle vorhanden Bilder auf, die aus dem Paket geladen werden können.
        """

        sounds = liste_dateien_rekursiv(self.resourcen_pfad, self.erlaubte_endungen)
        liste_ausgeben(sounds)

    def paket_lizenzen(self):
        """
        Lädt die Lizenzsinformationen zu den in pyenguin mitgelieferten Sounds.

        :return: Liste mit Lizenzinfos
        :rtype: list[str]
        """

        lizensen = [lese_datei(self.resourcen_pfad + "license.txt", ordner_pfad())]
        return lizensen

    def hat(self, schluessel):
        return schluessel in self.speicher

    def neue_instanz(self, pfad):
        raise NotImplemented("Muss überschrieben werden.")


class _SoundSpeicher(_Speicher):
    def __init__(self):
        super().__init__("resourcen/sounds", ("wav", "ogg"))

    def gib(self, schluessel):
        """

        :param schluessel:
        :type schluessel:
        :return:
        :rtype: Sound
        """
        return super().gib(schluessel)

    def neue_instanz(self, pfad):
        return Sound(pfad)


class _BildSpeicher(_Speicher):
    lade_mit_alpha = True

    def __init__(self):
        super().__init__("resourcen/bilder", ("png"))

    def neue_instanz(self, pfad):
        return self._lade_pygbild_aus_datei(pfad, self.lade_mit_alpha)

    @staticmethod
    def _lade_pygbild_aus_datei(pfad, alpha=True):
        """
        Lädt das Bild aus der beschrieben Datei.
        ACHTUNG: Kann das Bild nicht geladen werden, wird ein Fehler geworfen!

        :param pfad: Pfad des Bildes, das geladen werden soll
        :type pfad: str
        :param alpha: Falls das Bild Transparenz unterstüzten soll
        :type alpha: bool
        :return: die pygame Surface
        :rtype: pygame.Surface
        """

        if not existiert_datei(pfad):
            raise AttributeError("Die Datei '%s' existiert nicht." % pfad)

        try:
            pyg_bild = pygame.image.load(pfad)
        except pygame.error as e:
            print("Fehler beim Laden des Bildes: ", e)
            raise AttributeError("Das Bild: %s konnte nicht geladen werden!" % pfad)

        # laut Doku soll convert() aufgerufen werden?!
        if alpha:
            pyg_bild = pyg_bild.convert_alpha()
        else:
            pyg_bild = pyg_bild.convert()

        return pyg_bild

    def gib_pygame_bild(self, schluessel):
        return self.speicher[schluessel]

    def gib(self, schluessel):
        """

        :param schluessel:
        :type schluessel:
        :return:
        :rtype: Flaeche
        """
        return super().gib(schluessel)

    def _gib_speicher_element(self, schluessel):
        pyg_flaeche = self.speicher[schluessel]
        return Flaeche(pyg_flaeche.get_width(), pyg_flaeche.get_height(), pyg_flaeche)


SoundSpeicher = _SoundSpeicher()
BildSpeicher = _BildSpeicher()

if __name__ == "__main__":
    BildSpeicher.liste_im_paket()
    BildSpeicher.lade_aus_paket("a", "gegner/blocker.png")
    liste_ausgeben(BildSpeicher.paket_lizenzen())

    SoundSpeicher.liste_im_paket()
    SoundSpeicher.lade_aus_paket("a", "a_ton.wav")
    s = SoundSpeicher.gib("a")
    s.play()
    l = SoundSpeicher.paket_lizenzen()
    liste_ausgeben(l)
