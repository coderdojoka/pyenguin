from pyenguin.bbox import Box

__author__ = 'Mark Weinreuter'


class Sichtbar:
    def __init__(self):
        self.sichtbar = True

    def zeichne(self, flaeche):
        raise NotImplemented("zeichne() muss überschrieben werden in: %s" % str(self))


class SzenenDing:
    ANZAHL = 0

    @classmethod
    def nummer(cls):
        cls.ANZAHL += 1
        return str(cls.ANZAHL)

    def __init__(self, prefix=None):
        if prefix is None:
            prefix = str(self.__class__.__name__)
        self.name = prefix + SzenenDing.nummer()

        self.szene = None
        """
        Die Szene zu der dieses Objekt gehört.

        :type: szene.Szene
        """

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()


class ElterDing(SzenenDing):
    def __init__(self, prefix=None, elter=None):
        super().__init__(prefix)

        if elter is None:
            from pyenguin import szene
            elter = szene.Szene.fenster_szene

        self._elter = None
        """
        Die Szene oder Gruppe, in der dieses Element liegt.

        :type: pyenguin.zeichnen.SzenenListe
        """

        elter.dazu(self)


class Aktualisierbar(SzenenDing):
    def __init__(self, szene=None):
        super().__init__()

        self.ist_entfernt = False

        if szene is None:
            from pyenguin import szene
            szene = szene.Szene.fenster_szene

        self.szene = szene
        self.szene.registriere_aktualiserbar(self)

    def __del__(self):
        if not self.ist_entfernt:
            self.szene.entferne_aktualiserbar(self)

    def entferne(self):
        self.szene.entferne_aktualiserbar(self)
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


class SichtbaresSzenenDing(ElterDing, Sichtbar):
    def __init__(self, elter=None):
        Sichtbar.__init__(self)
        ElterDing.__init__(self, elter=elter)


class SzenenListe(ElterDing):
    def __init__(self, elter=None):
        super().__init__(elter=elter)

        self.liste = []
        """
        :type: list[all.BewegbaresSzenenDing]
        """

    def dazu(self, was):
        if not isinstance(was, ElterDing):
            print("%s kann nicht hinzufügt werden!" % str(was))
            return

        alte_liste = was._elter
        if alte_liste is not None:
            alte_liste.raus(was)

        was._elter = self
        self.liste.append(was)
        was.szene = self.szene

    def raus(self, was):
        if was in self.liste:
            self.liste.remove(was)
        else:
            print("%s ist nicht in dieser Gruppe." % str(was))


class Bewegbar(Box):
    def __init__(self, breite, hoehe):
        Box.__init__(self, 0, 0, breite, hoehe)
        self._welt_x_off = 0
        self._welt_y_off = 0

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
        return self._welt_x_off + self._x

    @property
    def welt_y(self):
        return self._welt_y_off + self._y

    def aktualisiere(self, dt):
        self.aendere_position(dt * self._x_bewegung, dt * self._y_bewegung)

    def anhalten(self):
        self._x_bewegung = 0
        self._y_bewegung = 0

    def __str__(self):
        return ": Pos: %d(%d), %d(%d), %dx%d" % (self._x, self._welt_x_off, self._y, self._welt_y_off, self.width, self.height)

    def bewegt(self):
        """
        Aufgerufen, wenn sich die Position geändert hat.

        :return:
        :rtype:
        """
        pass


class BewegbaresSzenenDing(Bewegbar, SichtbaresSzenenDing):
    def __init__(self, breite, hoehe, elter=None):
        SichtbaresSzenenDing.__init__(self, elter=elter)
        Bewegbar.__init__(self, breite, hoehe)
        self.setze_position(self.szene.breite/2, self.szene.hoehe/2)

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

        for element in self.liste:
            element._welt_x_off = x_off
            element._welt_y_off = y_off
            element.aktualisiere(dt)

    def zeichne(self, flaeche):
        if not self.sichtbar:
            return

        for element in self.liste:
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
