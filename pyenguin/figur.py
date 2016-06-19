from pyenguin.dinge import Gruppe, Bewegbar
from pyenguin.objekte import BewegbaresSzenenDing

__author__ = 'Mark Weinreuter'


class Figur(Gruppe):
    def __init__(self, objekte, elter=None):
        self._aktuelles_objekt = None
        self._aktueller_index = 0

        Gruppe.__init__(self, elter=elter)
        self.neue_kostueme(objekte)

    def aktualisiere(self, dt):
        Bewegbar.aktualisiere(self, dt)
        self._aktuelles_objekt.aktualisiere(dt)

    def zeichne(self, flaeche):
        flaeche.pyg_flaeche.blit(
            self._aktuelles_objekt.pyg_flaeche,
            (self._welt_x_off + self.links - self._aktuelles_objekt.halbe_breite,
             self._welt_y_off + self.oben - self._aktuelles_objekt.halbe_hoehe),
            self._aktuelles_objekt.ausschnitt)

    def neue_kostueme(self, objekte):
        if isinstance(objekte, BewegbaresSzenenDing):
            objekte = [objekte]

        for o in objekte:
            if not isinstance(o, BewegbaresSzenenDing):
                raise AttributeError("Kann %s (%s) nicht hinzufügen! Es muss zeichenbar sein." % (str(o), str(type(o))))

            self.dazu(o)

        self._aktuelles_objekt = self.kind_elemente[self._aktueller_index]
        return self._aktuelles_objekt.breite, self._aktuelles_objekt.hoehe

    def naechstes(self):
        self.zeige_nummer(self._aktueller_index + 1)

    def vorheriges(self):
        self.zeige_nummer(self._aktueller_index - 1)

    def zeige_nummer(self, index):
        self._aktueller_index = index % self.anzahl
        self._aktuelles_objekt = self.kind_elemente[self._aktueller_index]
        self.setze_dimension(self._aktuelles_objekt.breite, self._aktuelles_objekt.hoehe)

    def __hash__(self):
        return self.name.__hash__()
