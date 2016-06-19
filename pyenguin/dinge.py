from pyenguin.bbox import Bewegbar

__author__ = 'Mark Weinreuter'


class SzenenDing:
    """
    Kleinste Einheit, die zu einer Szene gehört.
    Diese hat einen Verweis, auf die dazugehörige Szene und  einen eindeutigen Namen.
    """
    ANZAHL = 0

    @classmethod
    def nummer(cls):
        cls.ANZAHL += 1
        return str(cls.ANZAHL)

    def __init__(self, prefix=None, elter=None):
        if prefix is None:
            prefix = str(self.__class__.__name__)
        self.name = prefix + SzenenDing.nummer()

        self.szene = None
        """
        Die Szene zu der dieses Objekt gehört.

        :type: szene.Szene
        """
        self.sichtbar = True

        if elter is None:
            from pyenguin import szene
            elter = szene.Szene.fenster_szene

        self._elter = None
        """
        Die Szene oder Gruppe, in der dieses Element liegt.

        :type: pyenguin.zeichnen.SzenenListe
        """

        # Setzt den Elternverweis
        elter.dazu(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()


class Aktualisierbar(SzenenDing):
    def __init__(self, szene=None):
        super().__init__()

        self.sichtbar = False
        self.ist_entfernt = False

    def __del__(self):
        if not self.ist_entfernt:
            self.szene.raus(self)

    def entferne(self):
        self.szene.raus(self)
        self.ist_entfernt = True

    def aktualisiere(self, dt):
        raise NotImplemented("Muss überschrieben werden!")


class Warte(Aktualisierbar):
    def __init__(self, dauer, was, wiederhole=False):
        super().__init__()
        self.was = was
        self.dauer = dauer
        self.wiederhole = wiederhole
        self._vergangene_zeit_ms = 0

    def aktualisiere(self, dt):
        self._vergangene_zeit_ms += dt

        # Ist die Zeit um?
        if self._vergangene_zeit_ms >= self.dauer:
            self.was()

            if self.wiederhole:
                self._vergangene_zeit_ms = 0
            else:
                self.entferne()


class SzenenListe(SzenenDing):
    def __init__(self, elter=None):
        super().__init__(elter=elter)

        self.kind_elemente = []
        """
        :type: list[all.BewegbaresSzenenDing]
        """
        self.anzahl = 0

    def dazu(self, was):
        if not isinstance(was, SzenenDing):
            print("%s kann nicht hinzufügt werden!" % str(was))
            return

        alte_liste = was._elter
        if alte_liste is not None:
            alte_liste.raus(was)

        was._elter = self
        self.kind_elemente.append(was)
        self.anzahl += 1
        was.szene = self.szene

    def raus(self, was):
        if was in self.kind_elemente:
            self.kind_elemente.remove(was)
            self.anzahl -= 1
        else:
            print("%s ist nicht in %s." % (str(was), str(self)))


class BewegbaresSzenenDing(Bewegbar, SzenenDing):
    def __init__(self, breite, hoehe, elter=None):
        self.bei_maus_klick = None

        SzenenDing.__init__(self, elter=elter)
        Bewegbar.__init__(self, breite, hoehe)
        self.setze_position(self.szene.breite / 2, self.szene.hoehe / 2)

    def setze_bei_maus_klick(self, funktion):
        self.bei_maus_klick = funktion
        self.szene.neues_maus_klick_ding(self)

    def entferne_bei_maus_klick(self):
        self.bei_maus_klick = lambda: None
        self.szene.entferne_maus_klick_ding(self)

    @property
    def abstand_rechts(self):
        return self.szene.breite - self.rechts

    @abstand_rechts.setter
    def abstand_rechts(self, wert):
        self.rechts = self.szene.breite - wert

    @property
    def abstand_links(self):
        return self.links

    @abstand_links.setter
    def abstand_links(self, wert):
        self.links = wert

    @property
    def abstand_unten(self):
        return self.szene.hoehe - self.unten

    @abstand_unten.setter
    def abstand_unten(self, wert):
        self.unten = self.szene.hoehe - wert

    @property
    def abstand_oben(self):
        return self.oben

    @abstand_oben.setter
    def abstand_oben(self, wert):
        self.oben = wert

    def raus_links(self):
        return self._welt_x_off + self.links < 0

    def ist_rechts_raus(self):
        return self._welt_x_off + self.rechts > self.szene.breite

    def ist_oben_raus(self):
        return self._welt_y_off + self.oben < 0

    def ist_unten_raus(self):
        return self._welt_y_off + self.unten > self.szene.hoehe

    def ist_raus(self):
        return self.raus_links() or self.ist_rechts_raus() or self.ist_oben_raus() or self.ist_unten_raus()

    def ist_linksrechts_raus(self):
        return self.raus_links() or self.ist_rechts_raus()

    def ist_obenunten_raus(self):
        return self.ist_oben_raus() or self.ist_unten_raus()

    def __str__(self):
        return self.name + ": Pos: %d(%d), %d(%d), %dx%d" % (self._x, self._welt_x_off, self._y, self._welt_y_off, self.width, self.height)


class Gruppe(BewegbaresSzenenDing, SzenenListe):
    def __init__(self, elter=None):
        BewegbaresSzenenDing.__init__(self, 0, 0, elter=elter)
        SzenenListe.__init__(self)

    def aktualisiere(self, dt):
        super().aktualisiere(dt)

        x_off = self._welt_x_off + self._x
        y_off = self._welt_y_off + self._y

        for element in self.kind_elemente:
            element._welt_x_off = x_off
            element._welt_y_off = y_off
            element.aktualisiere(dt)

    def zeichne(self, flaeche):
        if not self.sichtbar:
            return

        for element in self.kind_elemente:
            if element.sichtbar:
                element.zeichne(flaeche)


if __name__ == "__main__":
    b = BewegbaresSzenenDing(10, 10)
    b2 = BewegbaresSzenenDing(50, 50)
    b2.x = 100
    b2.y = -30
    g = Gruppe()

    print(b)

    b._x_bewegung = 10
    g._x_bewegung = -10
    b.name = "Boxi"
    g.dazu(b)

    print(b)
    print(b)
