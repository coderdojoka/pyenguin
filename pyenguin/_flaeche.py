import pygame

__author__ = 'Mark Weinreuter'


def neue_pygame_flaeche(breite, hoehe, alpha=False):
    """
    Erstellt einen neues pygame.Surface Objekt, das intern zum Zeichnen verwendet wird.
    :param breite:
    :type breite: int
    :param hoehe:
    :type hoehe: int
    :param alpha:
    :type alpha: bool
    :return:
    :rtype:pygame.Surface
    """
    if alpha:
        flaeche = pygame.Surface([breite, hoehe], pygame.SRCALPHA, 32)
        """:type:pygame.Surface"""
        flaeche.convert_alpha()
    else:
        flaeche = pygame.Surface([breite, hoehe])
        flaeche.convert()

    return flaeche


class _Flaeche():
    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=False):
        if pyg_flaeche is None:
            pyg_flaeche = neue_pygame_flaeche(breite, hoehe, alpha=transparent)

        self._pyg_flaeche = pyg_flaeche

    def zeichne(self, flaeche):
        flaeche._pyg_flaeche.blit(self._pyg_flaeche, self)

    def fuelle(self, farbe):
        self._pyg_flaeche.fill(farbe)

    def blit(self, flaeche, pos):
        self._pyg_flaeche.blit(flaeche._pyg_flaeche, pos)

    def blit_pyg_flaeche(self, pyg_flaeche, pos):
        self._pyg_flaeche.blit(pyg_flaeche, pos)

    def text(self, text, x, y, schrift, farbe=(0, 0, 0), hintergrund=None):
        """

        :param text:
        :type text:
        :param x:
        :type x:
        :param y:
        :type y:
        :param schrift:
        :type schrift: Schrift
        :param farbe:
        :type farbe:
        :param hintergrund:
        :type hintergrund:
        :return:
        :rtype:
        """

        pyg_flaeche = schrift.render(text, True, farbe, hintergrund)
        self._pyg_flaeche.blit(pyg_flaeche, (x, y))

    def bild(self, schluessel, x, y):
        from pyenguin.speicher import BildSpeicher
        pyg_bild = BildSpeicher.gib_pygame_bild(schluessel)
        self._pyg_flaeche.blit(pyg_bild, (x, y))

    def rechteck(self, x, y, breite, hoehe, farbe, dicke):
        pygame.draw.rect(self._pyg_flaeche, farbe, (x, y, breite, hoehe), dicke)

    def kreis(self, x, y, radius, farbe, dicke=0):
        pygame.draw.circle(self._pyg_flaeche, farbe, (int(x + radius), int(y + radius)), radius, dicke)

    def oval(self, x, y, radius_breite, radius_hoehe, farbe, dicke=None):
        pygame.draw.ellipse(self._pyg_flaeche, farbe, (x, y, radius_breite * 2, radius_hoehe * 2), dicke)

    def linie(self, start_x, start_y, ende_x, ende_y, farbe, dicke=1):
        pygame.draw.line(self._pyg_flaeche, farbe, (start_x, start_y), (ende_x, ende_y), dicke)

    def vieleck(self, punkte, farbe, dicke=None):
        return pygame.draw.polygon(self._pyg_flaeche, farbe, punkte, dicke)

    def linien(self, punkte, farbe, geschlossen):
        return pygame.draw.aalines(self._pyg_flaeche, farbe, geschlossen, punkte, True)
