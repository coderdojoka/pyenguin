__author__ = 'Mark Weinreuter'
import pygame
import pygame.font


class Schrift:
    """
    Eine Schrift, die zum Darstellen von Text verwendet werden kann.
    """

    standard = None

    def __init__(self, schrift_groesse, schrift_art="arial", system_schrift=True):
        """

        :param schrift_groesse: Größe der Schrift
        :type schrift_groesse: int
        :param schrift_art: Der Name der Schrift, z.B. Arial
        :type schrift_art: str
        """

        self.schrift_art = schrift_art
        self.schrift_groesse = schrift_groesse

        if system_schrift:
            self._pyg_schrift = pygame.font.SysFont(schrift_art, schrift_groesse)
        else:
            self._pyg_schrift = pygame.font.Font(schrift_art, schrift_groesse)

    def berechne_groesse(self, text):
        """
        Gibt die Größe des Textes zurück.

        :param text:
        :type text:
        :return:
        :rtype:
        """
        return self._pyg_schrift.size(text)

    def render(self, text, aa, farbe, hintergrund):
        return self._pyg_schrift.render(text, aa, farbe, hintergrund)

    @classmethod
    def gib_vorhandene_schriftarten(cls):
        fonts = pygame.font.get_fonts()
        return fonts

    @classmethod
    def gib_standard_schrift(cls):
        if cls.standard is None:
            cls.standard = Schrift(16)

        return cls.standard

    @classmethod
    def gib_standard_schrift_name(cls):
        return pygame.font.get_default_font()
