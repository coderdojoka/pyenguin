from pyenguin.flaeche import Flaeche
from pyenguin.szene import Bewegbar
from pyenguin.szene import Gruppe

__author__ = 'Mark Weinreuter'


class Figur(Gruppe):
    def __init__(self, objekte):
        self._aktuelles_objekt = None
        """
        :type: Flaeche
        """
        self._aktueller_index = 0

        Gruppe.__init__(self)
        breite, hoehe = self.neue_kostueme(objekte)
        self.setze_dimension(breite, hoehe)

    def aktualisiere(self, dt):
        Bewegbar.aktualisiere(self, dt)
        self._aktuelles_objekt.aktualisiere(dt)

    def zeichne(self, flaeche):
        flaeche.pyg_flaeche.blit(
            self._aktuelles_objekt.pyg_flaeche,
            (self.welt_x_off + self.x - self._aktuelles_objekt.halbe_breite,
             self.welt_y_off + self.y - self._aktuelles_objekt.halbe_hoehe),
            self._aktuelles_objekt.ausschnitt)

    def neue_kostueme(self, objekte):
        if isinstance(objekte, Flaeche):
            objekte = [objekte]

        for o in objekte:
            if not isinstance(o, Flaeche):
                raise AttributeError("Kann %s (%s) nicht hinzufügen! Es muss eine Fläche sein." % (str(o), str(type(o))))

            o.x = 0
            o.y = 0
            self.dazu(o)

        self._aktuelles_objekt = self.kind_dinge[self._aktueller_index]
        return self._aktuelles_objekt.breite, self._aktuelles_objekt.hoehe

    def naechstes(self):
        self.zeige_nummer(self._aktueller_index + 1)

    def vorheriges(self):
        self.zeige_nummer(self._aktueller_index - 1)

    def zeige_nummer(self, index):
        self._aktueller_index = index % self.anzahl
        self._aktuelles_objekt = self.kind_dinge[self._aktueller_index]
        self.setze_dimension(self._aktuelles_objekt.breite, self._aktuelles_objekt.hoehe)

    def __hash__(self):
        return self.name.__hash__()
