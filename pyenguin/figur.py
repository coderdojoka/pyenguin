from pyenguin.dinge import BewegbaresSzenenDing
from pyenguin.speicher import BildSpeicher

__author__ = 'Mark Weinreuter'


class Figur(BewegbaresSzenenDing):
    def __init__(self, schluessel):
        self._pyg_bilder = []
        self._pyg_bilder_namen = {}
        self._anzahl_bilder = 0
        self._aktuelles_pyg_bild = None
        self._aktueller_index = 0
        self.wechsle_bilder = False
        self.wechsel_dauer = 1000
        self._vergangene_zeit_ms = -1

        super().__init__(*self.neue_bilder(schluessel))

    def aktualisiere(self, dt):
        super().aktualisiere(dt)

        if self.wechsle_bilder:

            self._vergangene_zeit_ms += dt

            # Ist die Zeit um?
            if self._vergangene_zeit_ms >= self.wechsel_dauer:
                self.naechstes_bild()
                self._vergangene_zeit_ms = 0

    def zeichne(self, flaeche):
        flaeche._pyg_flaeche.blit(self._aktuelles_pyg_bild, self)

    def neue_bilder(self, schluessel):
        if isinstance(schluessel, str):
            schluessel = [schluessel]

        for schl in schluessel:
            if not BildSpeicher.hat(schl):
                print("Das Bild: %s ist NICHT im Bildspeicher vorhanden!" % schl)
                continue

            self._pyg_bilder.append(BildSpeicher.gib_pygame_bild(schl))
            self._pyg_bilder_namen[schl] = self._anzahl_bilder
            self._anzahl_bilder += 1

        if len(self._pyg_bilder) == 0:
            raise ValueError("Es wurden keine Bilder geladen. Dies ist ein Fehler!")

        self._aktuelles_pyg_bild = self._pyg_bilder[self._aktueller_index]
        return self._aktuelles_pyg_bild.get_width(), self._aktuelles_pyg_bild.get_height()

    def naechstes_bild(self):
        self.zeige_nummer(self._aktueller_index + 1)

    def vorheriges_bild(self):
        self.zeige_nummer(self._aktueller_index - 1)

    def zeige_nummer(self, index):
        self._aktueller_index = index % self._anzahl_bilder
        self._aktuelles_pyg_bild = self._pyg_bilder[self._aktueller_index]

    def zeige_name(self, name):
        if name not in self._pyg_bilder_namen:
            print("Es ist kein Bild mit dem Namen '%s' geladen." % name)
            return

        self._aktueller_index = self._pyg_bilder_namen[name]
        self._aktuelles_pyg_bild = self._pyg_bilder[self._aktueller_index]
