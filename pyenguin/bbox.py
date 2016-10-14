import pygame

from pyenguin.ereignis import EreignisBearbeiter

__author__ = 'Mark Weinreuter'


def berechne_groesse_unused(punkte):
    x = punkte[0][0]
    y = punkte[0][1]
    breite = punkte[0][0]
    hoehe = punkte[0][1]

    for p in punkte:

        if p[0] < x:
            x = p[0]

        if p[0] > breite:
            breite = p[0]

        if p[1] < y:
            y = p[1]

        if p[1] > hoehe:
            hoehe = p[1]

    # größe anpassen
    breite -= x
    hoehe -= y

    return breite, hoehe


class Box(pygame.Rect):
    """
    Eine einfache Box (Rechteck) mit Position und Breite, Hoehe
    """

    def __init__(self, *args):
        super().__init__(*args)

        self._x = 0
        self._y = 0
        self._halbe_breite = self.width / 2
        self._halbe_hoehe = self.height / 2
        self.bewegt = lambda: None

    def __str__(self):
        return "Box(%d, %d, %d, %d)" % (self._x, self._y, self.width, self.height)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, wert):
        self._x = wert
        self.centerx = self._x
        self.bewegt()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, wert):
        self._y = wert
        self.centery = self._y
        self.bewegt()

    @property
    def breite(self):
        return self.width

    @property
    def hoehe(self):
        return self.height

    @property
    def halbe_breite(self):
        return self._halbe_breite

    @property
    def halbe_hoehe(self):
        return self._halbe_hoehe

    @property
    def links(self):
        return self._x - self._halbe_breite

    @links.setter
    def links(self, wert):
        self.x = wert + self._halbe_breite

    @property
    def links_unten(self):
        return self.links, self.unten

    @links_unten.setter
    def links_unten(self, wert):
        self.x = wert[0] + self._halbe_breite
        self.y = wert[1] - self._halbe_hoehe

    @property
    def rechts_unten(self):
        return self.links, self.unten

    @rechts_unten.setter
    def rechts_unten(self, wert):
        self.x = wert[0] - self._halbe_breite
        self.y = wert[1] - self._halbe_hoehe

    @property
    def rechts(self):
        return self._x + self._halbe_breite

    @rechts.setter
    def rechts(self, wert):
        self.x = wert - self._halbe_breite

    @property
    def oben(self):
        return self._y - self._halbe_hoehe

    @oben.setter
    def oben(self, wert):
        self.y = wert + self._halbe_hoehe

    @property
    def unten(self):
        return self._y + self._halbe_hoehe

    @unten.setter
    def unten(self, wert):
        self.y = wert - self._halbe_hoehe

    def setze_position(self, x, y):
        self._x = x
        self._y = y
        self.centerx = x
        self.centery = y
        self.bewegt()

    def aendere_position(self, x, y):
        self.setze_position(x + self._x, y + self._y)

    def punkt_innerhalb(self, point, py=None):
        if py is not None:
            return bool(self.collidepoint(point, py))
        else:
            return bool(self.collidepoint(point[0], point[1]))

    def box_beruehrt(self, box):
        return bool(self.colliderect(box))

    def verschmelzen(self, box):
        return self.union(box)

    def verschmelze_alle(self, liste):
        r = self.unionall(liste)

    def setze_dimension(self, breite, hoehe):
        self.width = breite
        self._halbe_breite = breite / 2
        self.height = hoehe
        self._halbe_hoehe = hoehe / 2

    def dimension(self):
        return self.width, self.height


class Bewegbar(Box):
    def __init__(self, breite, hoehe):
        Box.__init__(self, 0, 0, breite, hoehe)

        # Diese Werte werden beim aktualisieren des
        # Elternelements gesetzt
        self.welt_x_off = 0
        self.welt_y_off = 0

        self._x_bewegung = 0
        self._y_bewegung = 0

    @property
    def bewegung_x(self):
        return self._x_bewegung

    @bewegung_x.setter
    def bewegung_x(self, wert):
        self._x_bewegung = wert

    @property
    def bewegung_y(self):
        return self._y_bewegung

    @bewegung_y.setter
    def bewegung_y(self, wert):
        self._y_bewegung = wert

    @property
    def welt_x(self):
        return self.welt_x_off + self._x

    @property
    def welt_y(self):
        return self.welt_y_off + self._y

    def aktualisiere(self, dt):
        self.aendere_position(dt * self._x_bewegung, dt * self._y_bewegung)

    def anhalten(self):
        self._x_bewegung = 0
        self._y_bewegung = 0

    def __str__(self):
        return ": Pos: %d(%d), %d(%d), %dx%d" % (self._x, self.welt_x_off, self._y, self.welt_y_off, self.width, self.height)


if __name__ == "__main__":
    b = Box(10, 10, 100, 100)
    b2 = Box(12, 40, 5, 5)
    b3 = Box(pygame.Rect(2, 3, 4, 5))
    b.x = 40

    print(b)
    b.links = 50
    print(b)
    print(b.punkt_innerhalb(60, 60))
    print(b.box_beruehrt(b2))
    b2.links = b.links
    b2.oben = b.oben - 4
    print(b2, b)
    print(b.box_beruehrt(b2))
