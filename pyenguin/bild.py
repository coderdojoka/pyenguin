import pygame

from pyenguin.objekte import Flaeche
from .speicher import BildSpeicher
from pyenguin.ereignis import EreignisBearbeiter

__author__ = 'Mark Weinreuter'


class Bild(Flaeche):
    def __init__(self, bild, transparent=True, elter=None):

        if isinstance(bild, str):
            self._pygame_bild = BildSpeicher.gib_pygame_bild(bild)
        elif isinstance(bild, pygame.Surface):
            self._pygame_bild = bild
        else:
            raise ValueError("Bitte Schlüssel des Bildes im Bildspeicher angeben.")

        Flaeche.__init__(self, self._pygame_bild.get_width(), self._pygame_bild.get_height(),
                          self._pygame_bild, transparent=transparent, elter=elter)


GESTOPPT = 0
GESTARTET = 1
PAUSIERT = 2
ZEIGE_BILD = 3
STANDARD_ZEIT = 100


def generiere_namen_liste(namen_muster, von, bis):
    """
    Erstellt eine Liste von Namen. Der Name muss ein %d enthalten, dass durch die Zahlen 'von' - 'bis'
     ersetzt wird.
    :param namen_muster: das Namen Muster, z.B. bild_%d.png -> wird zu bild_[von...bis].png
    :type namen_muster: str
    :param von: Startwert
    :type von: int
    :param bis: Endwert
    :type bis: int
    :return: eine Liste mit den generierten Namen
    :rtype: list[str]
    """
    return [namen_muster % i for i in range(von, bis)]


class BildAnimation(Flaeche):
    """
    Zeigt einen Animation an, indem eine Liste von Bildern(ZeichenFlaechen) in angegeben Zeitabschnitten
    durch gewechselt werden.
    """

    def __init__(self, pygame_flaechen, wiederhole=False,
                 alpha=True, anzeige_dauer=STANDARD_ZEIT):
        """
        Ein neues Animationsobjekt.

        :param pygame_flaechen:
        :type pygame_flaechen: list[str|pygame.Surface]
        :param wiederhole:
        :type wiederhole: bool
        :param alpha:
        :type alpha: bool
        :param anzeige_dauer:
        :type anzeige_dauer: float
        :return:
        :rtype:
        """

        self._wiederhole_animation = wiederhole
        """
        Gibt an ob die Animation wiederholt wird oder nicht
        """
        self._pyg_flaechen = []
        """
        :type: list[(ZeichenFlaeche, int)]
        """
        self._zeige_letztes_bild = False

        self._bild_gewechselt = EreignisBearbeiter()
        self._animation_gestartet = EreignisBearbeiter()
        self._animation_geendet = EreignisBearbeiter()

        self._gesamt_zeit = 0
        self._aktueller_index = 0
        self._zustand = GESTOPPT
        self._vergangen = 0
        self._gesamt_zeit = 0

        # zur Ermittlung der Dimension
        breite = 0
        hoehe = 0

        for zf in pygame_flaechen:

            # Die Fläche kann entweder aus einer Datei/ dem Bildspeicher geladen werden
            if isinstance(zf, str):
                # Falls im Speicher, nehmen wir dieses Bild
                if BildSpeicher.hat(zf):
                    zf = BildSpeicher.gib_pygame_bild(zf)
                else:
                    # Ansonsten laden wir es
                    zf = BildSpeicher.lade_pygbild_aus_datei(zf, alpha)

            # oder schon eine pygame surface sein
            elif not isinstance(zf, pygame.Surface):
                raise AttributeError("Entweder Surface oder Strings übergeben.")

            # die größten werte ermitteln
            if zf.get_width() > breite:
                breite = zf.get_width()
            if zf.get_height() > hoehe:
                hoehe = zf.get_height()

            # Zur List hinzufügen und Zeit addieren
            self._pyg_flaechen.append(zf)

        self._anzahl_flaechen = len(self._pyg_flaechen)
        self.anzeige_dauer = anzeige_dauer
        self._gesamt_zeit = anzeige_dauer * self._anzahl_flaechen

        Flaeche.__init__(self, breite, hoehe, None)

    def start(self):
        if self._zustand == GESTOPPT or self._zustand == ZEIGE_BILD:
            self._vergangen = 0
            self._aktueller_index = 0

        self._zustand = GESTARTET
        self._animation_gestartet()

    def aktualisiere(self, dt):
        super().aktualisiere(dt)
        if self._zustand != GESTARTET:
            return

        self._vergangen += dt
        tmp_index = self._aktueller_index

        # solange die Zeit für das aktuelle Bild abgelaufen ist, gehe zum nächsten bild
        # Nur falls mehrere bilder übersprungen werden müssen
        while self._vergangen > self.anzeige_dauer:
            self._vergangen -= self.anzeige_dauer

            tmp_index += 1  # nächste fläche

            # alle Flächen gezeichnet?
            if tmp_index == self._anzahl_flaechen:

                if not self._wiederhole_animation:

                    self._animation_geendet()
                    if self._zeige_letztes_bild:
                        # animation anhalten
                        self.zeige_letztes_bild()

                        # damit genau dieses Bild gezeichnet wird
                        break
                    else:
                        self._zustand = GESTOPPT
                else:
                    self._aktueller_index = 0

                    self._animation_gestartet()

            # falls die animation läuft, müssen wir die bilder wechseln
            else:
                # sicher gehen, das wir einen korrekten index verwenden
                self._aktueller_index = tmp_index % self._anzahl_flaechen
                self._bild_gewechselt(self._aktueller_index)

            self.pyg_flaeche = self._pyg_flaechen[self._aktueller_index]

    def zeichne(self, flaeche):
        # in allen zuständen, außer gestoppt zeichnen wir
        if self._zustand != GESTOPPT:
            super().zeichne(flaeche)

    def zeige_letztes_bild_wenn_geendet(self, wert=True):
        """
        Wenn die Animation geendet hat, wird das letzte Bilder der Animation als Standbild angezeigt.
        Achtung: Dies ist nur möglich, wenn die Animation nicht wiederholt wird.

        :param wert:
        :type wert: bool
        """
        if self._wiederhole_animation:
            print("Bei wiederholenden Animationen ist dies nicht nicht möglich!")
            return

        self._zeige_letztes_bild = wert

    def zeige_bild(self, index):
        if index < 0 or index > len(self._pyg_flaechen):
            raise ValueError("Index muss größer 0 und kleiner als die Anzahl an Bildern sein")

        self._zustand = ZEIGE_BILD
        self._aktueller_index = index
        self.pyg_flaeche = self._pyg_flaechen[self._aktueller_index]

    def registriere_wenn_bild_gewechselt(self, wenn_gewechselt):
        self._bild_gewechselt.registriere(wenn_gewechselt)

    def registriere_wenn_gestartet(self, wenn_gestartet):
        self._animation_gestartet.registriere(wenn_gestartet)

    def registriere_wenn_geendet(self, wenn_geendet):
        self._animation_geendet.registriere(wenn_geendet)

    def setze_wiederhole(self, wiederhole=True):
        self._wiederhole_animation = wiederhole

    def stop(self):
        self._zustand = GESTOPPT

    def pause(self):
        self._zustand = PAUSIERT

    def zeige_erstes_bild(self):
        self.zeige_bild(0)

    def zeige_letztes_bild(self):
        self.zeige_bild(self._anzahl_flaechen - 1)
