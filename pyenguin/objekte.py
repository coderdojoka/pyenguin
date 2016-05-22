from pyenguin._flaeche import _Flaeche
from pyenguin.dinge import BewegbaresSzenenDing
from pyenguin.schrift import Schrift

__author__ = 'Mark Weinreuter'


class Flaeche(_Flaeche, BewegbaresSzenenDing):
    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=False, elter=None):
        BewegbaresSzenenDing.__init__(self, breite, hoehe, elter=elter)
        _Flaeche.__init__(self, breite, hoehe, pyg_flaeche, transparent)

        self.ausschnitt = None

    def als_bild_speichern(self, pfad):
        import pygame
        pygame.image.save(self._pyg_flaeche, pfad)

    def zeichne(self, flaeche):
        flaeche._pyg_flaeche.blit(self._pyg_flaeche, (self._welt_x_off + self.links, self._welt_y_off + self.oben),
                                  self.ausschnitt)


class Text(Flaeche):
    def __init__(self, text, schrift=None, farbe=(0, 0, 0), hintergrund=None, elter=None):
        if schrift is None:
            schrift = Schrift.gib_standard_schrift()

        breite, hoehe = schrift.berechne_groesse(text)

        self.schrift = schrift
        self.text = text
        self.hintergrund = hintergrund
        self.farbe = farbe

        pyg_flaeche = schrift.render(self.text, True, self.farbe, self.hintergrund)

        super().__init__(breite, hoehe, pyg_flaeche=pyg_flaeche, elter=elter)

    def setze_text(self, text):
        breite, hoehe = self.schrift.berechne_groesse(text)
        self.setze_dimension(breite, hoehe)
        self.text = text

        self._pyg_flaeche = self.schrift.render(self.text, True, self.farbe, self.hintergrund)
