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


class Bemalbar(object):
    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=False):
        """
        Eine neue Fläche, die Klasse sollte nicht direkt verwendet werden.

        :param breite:
        :type breite:
        :param hoehe:
        :type hoehe:
        :param pyg_flaeche:
        :type pyg_flaeche:
        :param transparent:
        :type transparent:
        """
        if pyg_flaeche is None:
            pyg_flaeche = neue_pygame_flaeche(breite, hoehe, alpha=transparent)

        self.pyg_flaeche = pyg_flaeche

    def zeichne(self, flaeche):
        flaeche._pyg_flaeche.blit(self.pyg_flaeche, self)

    def fuelle(self, farbe):
        self.pyg_flaeche.fill(farbe)

    def blit(self, flaeche, pos):
        self.pyg_flaeche.blit(flaeche.pyg_flaeche, pos)

    def blit_pyg_flaeche(self, pyg_flaeche, pos):
        self.pyg_flaeche.blit(pyg_flaeche, pos)

    def text(self, text, x, y, schrift, farbe=(0, 0, 0), hintergrund=None):
        """
        Zeichnet den gegegeben Text an der angegebenen Stelle in gewünschter Farbe.

        :param text:
        :type text:
        :param x: Die LINKE obere Koordinate
        :type x:
        :param y: DIE OBERE linke Koordinate
        :type y:
        :param schrift: Die zu verwendente Schriftart
        :type schrift: Schrift
        :param farbe:
        :type farbe:
        :param hintergrund:
        :type hintergrund:
        :return:
        :rtype:
        """

        pyg_flaeche = schrift.render(text, True, farbe, hintergrund)
        self.pyg_flaeche.blit(pyg_flaeche, (x, y))

    def bild(self, schluessel, x, y):
        from pyenguin.speicher import BildSpeicher
        pyg_bild = BildSpeicher.gib_pygame_bild(schluessel)
        self.pyg_flaeche.blit(pyg_bild, (x, y))

    def rechteck(self, x, y, breite, hoehe, farbe, dicke):
        pygame.draw.rect(self.pyg_flaeche, farbe, (x, y, breite, hoehe), dicke)

    def kreis(self, x, y, radius, farbe, dicke=0):
        pygame.draw.circle(self.pyg_flaeche, farbe, (int(x + radius), int(y + radius)), radius, dicke)

    def oval(self, x, y, radius_breite, radius_hoehe, farbe, dicke=None):
        pygame.draw.ellipse(self.pyg_flaeche, farbe, (x, y, radius_breite * 2, radius_hoehe * 2), dicke)

    def linie(self, start_x, start_y, ende_x, ende_y, farbe, dicke=1):
        pygame.draw.line(self.pyg_flaeche, farbe, (start_x, start_y), (ende_x, ende_y), dicke)

    def vieleck(self, punkte, farbe, dicke=None):
        return pygame.draw.polygon(self.pyg_flaeche, farbe, punkte, dicke)

    def linien(self, punkte, farbe, geschlossen):
        return pygame.draw.aalines(self.pyg_flaeche, farbe, geschlossen, punkte, True)
