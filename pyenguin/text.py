from pyenguin import *

__author__ = 'Mark Weinreuter'


class FesteBreiteText(Flaeche):
    def __init__(self, breite, schrift, text, hintergrund=WEISS, min_hoehe=0):
        self.zeilen = []
        self.zeilen_hoehe = []
        self.max_breite = breite
        self.schrift = schrift
        self.anzeige_text = text
        self.hintergrund = hintergrund
        self.min_hoehe = min_hoehe
        self.ignoriere_nach_umbruch = " \n\r"
        super().__init__(breite, self.verarbeite_text())

        self.male_text()

    def setze_text(self, text):
        self.anzeige_text = text
        h = self.verarbeite_text()
        self.aendere_groesse(self.max_breite, h)
        self.male_text()

    def verarbeite_text(self):
        ausprobieren = ""
        self.zeilen = []
        self.zeilen_hoehe = []
        ignoriere_leerzeichen = False
        hoehe = 0

        for buchstabe in self.anzeige_text:

            b, h = self.schrift.berechne_groesse(ausprobieren + buchstabe)
            # Wir fügen immer einen neuen Buchstaben an und überprüfen,
            # ob der Text noch in die Breite passt!
            if buchstabe == "\n" or b > self.max_breite:
                self.zeilen_hoehe.append(h)
                self.zeilen.append(ausprobieren)
                if buchstabe not in self.ignoriere_nach_umbruch:
                    ausprobieren = buchstabe
                else:
                    ausprobieren = ""
            else:
                ausprobieren += buchstabe

        # Restlichen Text einfügen
        b, h = self.schrift.berechne_groesse(ausprobieren)
        self.zeilen.append(ausprobieren)
        self.zeilen_hoehe.append(h)
        hoehe = sum(self.zeilen_hoehe)

        return max(hoehe, self.min_hoehe)

    def male_text(self):
        self.fuelle(self.hintergrund)
        y = 0
        for i in range(len(self.zeilen)):
            zeile = self.zeilen[i]
            self.text(zeile, 0, y, self.schrift)
            y += self.zeilen_hoehe[i]
