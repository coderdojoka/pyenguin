from pyenguin.szene import Ding, Szene

__author__ = 'Mark Weinreuter'


class Aktualisierbar(Ding):
    def __init__(self, szene):
        if szene is None:
            szene = Szene.fenster_szene

        super().__init__(szene=szene)
        self.szene.registriere_aktualisiere(self.aktualisiere)

    def entferne(self):
        self.szene.entferne_aktualisiere(self.aktualisiere)

    def aktualisiere(self, dt):
        raise AttributeError("Muss überschrieben werden!")

    def __call__(self, *args, **kwargs):
        self.aktualisiere(*args, **kwargs)


class Warte(Aktualisierbar):
    def __init__(self, dauer, was, wiederhole=False, szene=None):
        super().__init__(szene=szene)
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
