from pyenguin.bemalbar import Bemalbar
from pyenguin.dinge import BewegbaresSzenenDing
from pyenguin.schrift import Schrift

__author__ = 'Mark Weinreuter'


class Flaeche(Bemalbar, BewegbaresSzenenDing):
    """
    Eine einfach Fläche, auf der gezeichnet werden kann.
    Eine Fläche hat eine feste Breite und Höhe.
    """

    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=False, elter=None):
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
        :param elter: Das Elternobjekt in der Hierachie
        :type elter:
        """
        BewegbaresSzenenDing.__init__(self, breite, hoehe, elter=elter)
        Bemalbar.__init__(self, breite, hoehe, pyg_flaeche, transparent)

        self.ausschnitt = None

    def als_bild_speichern(self, pfad):
        """
        Speichert den aktuell gezeichneten Inhalt in einem PNG-Bild.


        :param pfad: Der Pfad unter dem das Bild gespeichert werden soll
        :type pfad: str
        """
        import pygame
        pygame.image.save(self.pyg_flaeche, pfad)

    def zeichne(self, flaeche):
        flaeche.pyg_flaeche.blit(self.pyg_flaeche, (self._welt_x_off + self.links, self._welt_y_off + self.oben),
                                  self.ausschnitt)

    def __hash__(self):
        return self.name.__hash__()


class Text(Flaeche):
    """
    Eine Fläche, auf der ein Text gezeichnet wird.
    """

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
        """
        Ändert den angezeigten Text und damit auch die Größe der Fläche.

        :param text: Der Text, der angezeigt werden soll
        :type text: str
        """
        breite, hoehe = self.schrift.berechne_groesse(text)
        self.setze_dimension(breite, hoehe)
        self.text = text

        self.pyg_flaeche = self.schrift.render(self.text, True, self.farbe, self.hintergrund)
