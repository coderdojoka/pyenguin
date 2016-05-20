import pygame

from pyenguin.helfer import kombiniere_pfad, ordner_pfad

__author__ = 'Mark Weinreuter'


class HintergrundMusik:
    RESOURCEN_MUSIK = "resourcen/musik/"

    @classmethod
    def lade_aus_paket(cls, pfad):
        pfad = kombiniere_pfad(ordner_pfad(), cls.RESOURCEN_MUSIK, pfad)
        cls.lade(pfad, ordner_pfad=pfad)

    @classmethod
    def lade(cls, pfad, ordner_pfad=""):
        pfad = kombiniere_pfad(ordner_pfad, pfad)
        pygame.mixer.music.load(pfad)

    @staticmethod
    def start(wiederholungen=0, versatz=0):
        pygame.mixer.music.play(loops=wiederholungen, start=versatz)

    @staticmethod
    def pause():
        pygame.mixer.music.pause()

    @staticmethod
    def weiter():
        pygame.mixer.music.unpause()

    @staticmethod
    def stop():
        pygame.mixer.music.pause()

    @staticmethod
    def gib_lautstaerke():
        return pygame.mixer.music.get_volume()

    @staticmethod
    def setze_lautstaerke(wert):
        return pygame.mixer.music.set_volume(wert)


class Sound(pygame.mixer.Sound):
    @staticmethod
    def pause():
        pygame.mixer.pause()

    @staticmethod
    def weiter():
        pygame.mixer.unpause()

    @staticmethod
    def aktive_sounds():
        return pygame.mixer.get_busy()

    def __init__(self, pfad):
        super().__init__(pfad)

    def start(self, wiederholungen=0, max_zeit=0, fade_zeit=0):
        self.play(wiederholungen, max_zeit, fade_zeit)

    def stop(self):
        self.stop()

    def gib_lautstaerke(self):
        return self.get_volume()

    def setze_lautstaerke(self, wert):
        self.set_volume(wert)

    def dauer(self):
        return self.get_length()
