from pyenguin.szene import SzenenDing

__author__ = 'Mark Weinreuter'


class Warte(SzenenDing):
    def __init__(self, dauer, was, wiederhole=False):
        super().__init__()
        self.sichtbar = False
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
