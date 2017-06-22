import pygame
import pygame.font

from pyenguin.szene import BewegbaresSzenenDing

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


def klone_pygame_flaeche(pyg_flaeche, alpha=False):
    """
    Erstellt einen neues pygame.Surface Objekt, das intern zum Zeichnen verwendet wird.

    :return:
    :rtype:pygame.Surface
    """
    if alpha or pyg_flaeche.get_alpha() is not None:
        flaeche = pygame.Surface([pyg_flaeche.get_width(), pyg_flaeche.get_height()], pygame.SRCALPHA, 32)
        """:type:pygame.Surface"""
        flaeche.convert_alpha()
    else:
        flaeche = pygame.Surface([pyg_flaeche.get_width(), pyg_flaeche.get_height()])
        flaeche.convert()

    return flaeche


class Leinwand(object):
    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=True):
        """
        Erstellt eine neue Leinwand mit entweder der angegebenen Breite und Höhe,
        oder von der übergebenen pyg_flaeche.

        :param breite: Die Breite der Fläche
        :type breite: int
        :param hoehe: Die Höhe der Fläche
        :type hoehe: int
        :param pyg_flaeche: (Optional) Die Fläche
        :type pyg_flaeche: pygame.Surface
        :param transparent: Falls die Fläche transparent erstellt werden soll.
        :type transparent: bool
        """

        self.ausschnitt = None

        if pyg_flaeche is None:
            pyg_flaeche = neue_pygame_flaeche(breite, hoehe, alpha=transparent)

        self.pyg_flaeche = pyg_flaeche

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

    def rechteck(self, x, y, breite, hoehe, farbe, dicke=0):
        pygame.draw.rect(self.pyg_flaeche, farbe, (x, y, breite, hoehe), dicke)

    def kreis(self, x, y, radius, farbe, dicke=0):
        pygame.draw.circle(self.pyg_flaeche, farbe, (int(x + radius), int(y + radius)), radius, dicke)

    def oval(self, x, y, radius_breite, radius_hoehe, farbe, dicke=0):
        pygame.draw.ellipse(self.pyg_flaeche, farbe, (x, y, radius_breite * 2, radius_hoehe * 2), dicke)

    def linie(self, start_x, start_y, ende_x, ende_y, farbe, dicke=1):
        pygame.draw.line(self.pyg_flaeche, farbe, (start_x, start_y), (ende_x, ende_y), dicke)

    def vieleck(self, punkte, farbe, dicke=0):
        return pygame.draw.polygon(self.pyg_flaeche, farbe, punkte, dicke)

    def linien(self, punkte, farbe, geschlossen):
        return pygame.draw.aalines(self.pyg_flaeche, farbe, geschlossen, punkte, True)

    def als_bild_speichern(self, pfad):
        """
        Speichert den aktuell gezeichneten Inhalt in einem PNG-Bild.


        :param pfad: Der Pfad unter dem das Bild gespeichert werden soll
        :type pfad: str
        """
        import pygame
        pygame.image.save(self.pyg_flaeche, pfad)


class Flaeche(BewegbaresSzenenDing, Leinwand):
    """
    Eine einfach Fläche, auf der gezeichnet werden kann.
    Eine Fläche hat eine feste Breite und Höhe.
    """

    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=True, szene=None):
        """
        Erstellt eine neue Fläche mit entweder der angegebenen Breite und Höhe,
        oder von der übergegebnen pyg_flaeche.

        :param breite: Die Breite der Fläche
        :type breite: int
        :param hoehe: Die Höhe der Fläche
        :type hoehe: int
        :param pyg_flaeche: (Optional) Die Fläche
        :type pyg_flaeche: pygame.Surface
        :param transparent: Falls die Fläche transparent erstellt werden soll.
        :type transparent: bool
        :param szene: Das Elternobjekt in der Hierachie
        :type szene:
        """
        Leinwand.__init__(self, breite, hoehe, pyg_flaeche, transparent)
        BewegbaresSzenenDing.__init__(self, breite, hoehe, szene=szene)

        self.ausschnitt = None

        self.original_pyg_flaeche = self.pyg_flaeche
        self.winkel = 0
        self.skalierung = 1

    def aendere_groesse(self, breite, hoehe, transparent=True):
        self.pyg_flaeche = neue_pygame_flaeche(breite, hoehe, alpha=transparent)
        self.original_pyg_flaeche = self.pyg_flaeche
        self.setze_dimension(breite, hoehe)

    def setze_rotation(self, winkel, smooth=True):
        """
        Rotiert das Objekt auf den angegeben Winkel.
        :param winkel:
        :type winkel:
        :return:
        :rtype:
        """
        self.winkel = winkel
        self._rotiere_und_skaliere(smooth)

    def rotiere(self, winkel, smooth=True):
        """
        Rotiert das Objekt um den angegeben Winkel. Vorherige Rotationen werden mit in Betracht gezogen!

        :param winkel:
        :type winkel:
        :return:
        :rtype:
        """
        self.winkel += winkel
        self._rotiere_und_skaliere(smooth)

    def setze_skalierung(self, skalierung, smooth=True):
        """
        Skaliert das Objekt auf den angegeben Wert.

        :param skalierung:
        :type skalierung:
        :return:
        :rtype:
        """
        self.skalierung = skalierung
        self._rotiere_und_skaliere(smooth)

    def skaliere(self, skalierung, smooth=True):
        """
        Rotiert das Objekt um den angegeben Winkel. Vorherige Rotationen werden mit in Betracht gezogen!
        :param skalierung:
        :type skalierung:
        :return:
        :rtype:
        """
        self.skalierung *= skalierung
        self._rotiere_und_skaliere(smooth)

    def setze_rotation_und_skalierung(self, winkel, skalierung, smooth=True):
        """
        Skaliert und rotiert das Objekt auf den angegeben Wert.

        :param winkel:
        :type winkel:
        :param skalierung:
        :type skalierung:
        :return:
        :rtype:
        """
        self.winkel = winkel
        self.skalierung = skalierung
        self._rotiere_und_skaliere(smooth)

    def _rotiere_und_skaliere(self, smooth=True):
        if self.original_pyg_flaeche == self.pyg_flaeche:
            self.pyg_flaeche = klone_pygame_flaeche(self.original_pyg_flaeche, True)

        if smooth:
            self.pyg_flaeche = pygame.transform.rotozoom(self.original_pyg_flaeche, self.winkel, self.skalierung)
        else:
            self.pyg_flaeche = pygame.transform.scale(self.pyg_flaeche, (int(self.width * self.skalierung), int(self.height * self.skalierung)))
            self.pyg_flaeche = pygame.transform.rotate(self.original_pyg_flaeche, self.winkel)

        # das umgebende Rechteck hat sich geändert => Bild Zentrum anpassen
        w, h = self.pyg_flaeche.get_width(), self.pyg_flaeche.get_height()
        self.setze_dimension(w, h)

    def zeichne(self, flaeche):
        flaeche.pyg_flaeche.blit(self.pyg_flaeche, (self.welt_x_off + self.links,
                                                    self.welt_y_off + self.oben), self.ausschnitt)


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


class Text(Flaeche):
    """
    Eine Fläche, auf der ein Text gezeichnet wird.
    """

    def __init__(self, text, schrift=None, farbe=(0, 0, 0), hintergrund=None):
        """
        Erstellt einen Text, der angezeigt wird.

        :param text: Der angezeigte Text
        :type text: str
        :param schrift: Gewünschte Schrift (optional)
        :type schrift: Schrift
        :param farbe: Schriftfarbe (optional, Schwarz ist Standard)
        :type farbe: tuple(int)
        :param hintergrund: Hintergrundfarbe (optional)
        :type hintergrund:
        """
        if schrift is None:
            schrift = Schrift.gib_standard_schrift()

        breite, hoehe = schrift.berechne_groesse(text)

        self.schrift = schrift
        self.__text = text
        self.__hintergrund = hintergrund
        self.__farbe = farbe

        pyg_flaeche = schrift.render(self.__text, True, self.__farbe, self.__hintergrund)

        super().__init__(breite, hoehe, pyg_flaeche=pyg_flaeche)

    def setze_farbe(self, farbe, hintergrund=(-1, -1, -1)):
        """
        Ändert die Textfarbe und ggf. die Hintergrundfarbe.

        :param farbe:
        :type farbe:
        :param hintergrund: Hintergrundfarbe (optional)
        :type hintergrund:

        :return:
        :rtype:
        """
        self.__farbe = farbe
        if hintergrund != (-1, -1, -1):
            self.__hintergrund = hintergrund

        self.setze_text(self.__text)

    def gib_farbe(self):
        return self.__farbe

    def setze_text(self, text):
        """
        Ändert den angezeigten Text und damit auch die Größe der Fläche.
        **Achtung**: Dies ändert die Position des Textes! Der Text muss neu positioniert werden.

        :param text: Der Text, der angezeigt werden soll
        :type text: str
        """

        self.__text = text
        self.pyg_flaeche = self.schrift.render(self.__text, True, self.__farbe, self.__hintergrund)
        self.setze_dimension(self.pyg_flaeche.get_width(), self.pyg_flaeche.get_height())
