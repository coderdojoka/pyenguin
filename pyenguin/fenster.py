import logging
import sys

import pygame
from pyenguin.ereignis import EreignisBearbeiter
from pyenguin.gitter import Gitter
from pyenguin.szene import Szene
from pygame.constants import QUIT, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, KEYUP, K_ESCAPE

__author__ = 'Mark Weinreuter'

logger = logging.getLogger(__name__)

pygame.mixer.pre_init(44100, 16, 2, 2048)  # setup mixer to avoid sound lag
pygame.init()
pygame.font.init()


class FensterOptionen:
    def __init__(self, breite=640, hoehe=480, titel="Mein Fenster", vollbild=False, aktualisiere=lambda: None, esc_taste=True):
        self.titel = titel
        self.breite = breite
        self.hoehe = hoehe
        self.vollbild = vollbild
        self.aktualisiere = aktualisiere
        self.esc_taste = esc_taste
        self.fps = 30


class Fenster:
    """
    Die Klasse, um ein Fenster anzuzeigen und die Schleife zu starten.
    Nachdem einen Instanz erstellt wurde, muss :py:meth:`~Fenster.starten()` aufgerufen werden,
    um das Fenser zu starten.:

        fenster = Fenster(400, 600, "Hallo Fenster)
        # ... Elemente und Ereignisse erstellen/registrieren

        fenster.starten()

    """

    aktuelles_fenster = None
    """
    Das aktuelle Fenster

    :type: pyenguin.fenster.Fenster
    """

    zeit_unterschied_ms = 0
    """
    Der Zeitunterschied zwischen den aktuellen Frames.

    :type: float
    """

    relativer_unterschied = 0
    """
    Der relative Zeitunterschied zwischen den aktuellen Frames.

    :type: float
    """

    def __init__(self, breite=640, hoehe=480, titel="pyenguin Zeichenbibliothek", flags=0):
        """
        Initialisiert das Fenster.

        :param breite: die Fensterbreite
        :type breite: int
        :param hoehe: die Fensterhöhe
        :type hoehe: int
        :param titel: Der Fenstertitel
        :type titel: str
        :param aktualisierungs_funktion: die Aktualisierungsfunktion,
         die bei jedem Neuzeichnen aufgerufen wird (fps mal pro sekunde)
        :type aktualisierungs_funktion: (float) -> None
        """

        self.breite = breite
        """
        Die Breite des Spiels (Fensters).
    
        :type: int
        """
        self.hoehe = hoehe
        """
        Die Höhe des Spiels (Fensters).
    
        :type: int
        """
        self.fps = 30
        """
        Die Anzahl der Aktualisierungen pro Sekunde ("Frames per second).
    
        :type: float
        """

        self._ist_aktiv = True
        """
        Solange dieses Flag auf True gesetzt ist, läuft die Spiel.

        :type: bool
        """

        self._clock = pygame.time.Clock()
        """
        Taktgeber für das Spiel um die Fps einzustellen.
    
        :type: pygame.time.Clock
        """

        self.__aktualisiere = EreignisBearbeiter()
        """
        Die Funktion, die aufgerufen wird, wenn das Spiel aktualisiert wird (fps mal).
    
        :type: pyenguin.EreignisBearbeiter
        """

        # Dimension des Fensters
        self.breite = breite
        self.hoehe = hoehe

        # Fenstertitel
        self.setze_fenster_titel(titel)

        # Die Hauptszene
        Szene.init(Szene(breite, hoehe, pygame.display.set_mode((breite, hoehe), flags),
                         farbe=(255, 255, 255)))

        # setze ESC handler um das Fenster zu schließen
        Szene.fenster_szene.registriere_taste_unten(K_ESCAPE, lambda taste: self.beenden())

        # Wir sind das aktuelle Fenster (THERE can only be ONE!!!)
        if Fenster.aktuelles_fenster is not None:
            raise AttributeError("Es kann NUR EIN Fenster geben!")

        Fenster.aktuelles_fenster = self

    def beenden(self, erzwingen=False):
        """
        Beendet und schließt das Fenster.
        """
        if self.darf_beendet_werden() or erzwingen:
            self._ist_aktiv = False

    def darf_beendet_werden(self):
        """
        Funktion die aufgerufen wird, wenn das Spiel beendet wird.


        :return: True, falls das Fenster geschlossen
        :rtype: bool
        """

        return True

    def starten(self):
        """
        Startet das Fenster. Hinweis, diese Funktion blockiert und kehrt nie zurück!
        """

        # erster tick für zeit_unterschied_ms
        self._clock.tick(self.fps)

        while self._ist_aktiv:  # self schleife

            # wir gehen alle events durch
            for ereignis in pygame.event.get():

                # Fenster schließen
                if ereignis.type == QUIT:
                    self.beenden()

                # Maus bewegt
                elif ereignis.type == MOUSEMOTION:
                    Szene.verarbeite_maus_bewegt(ereignis)

                # Maustaste gedrückt
                elif ereignis.type == MOUSEBUTTONDOWN:
                    Szene.verarbeite_maus_geklickt(ereignis)

                # Maustaste losgelassen
                elif ereignis.type == MOUSEBUTTONUP:
                    Szene.verarbeite_maus_losgelassen(ereignis)

                elif ereignis.type == KEYDOWN:
                    Szene.verarbeite_taste_unten(ereignis)

                elif ereignis.type == KEYUP:
                    Szene.verarbeite_taste_oben(ereignis)

            # Alles zeichnen und für Aktualisierung sorgen
            self._aktualisiere_und_zeichne()

            # muss aufgerufen werden um Änderungen anzuzeigen
            pygame.display.flip()  # update besser?

        # Die Schleife ist zu Ende, wir beenden das Programm :)
        pygame.quit()
        sys.exit()

    def _aktualisiere_und_zeichne(self):
        # lässt das self mit ca. dieser fps laufen und fragt vergangene Zeit ab
        self.zeit_unterschied_ms = self._clock.tick(self.fps)

        # relativer Zeitunterschied
        self.relativer_unterschied = self.zeit_unterschied_ms / self.fps

        # Alle registrierten Aktualisierungs-Funktionen
        self.__aktualisiere(self.relativer_unterschied)

        # Alle Instanzen, die von Aktualisierbar erben
        # Aktualisierbar.aktualisiere_alle(self.relativer_unterschied, self.zeit_unterschied_ms)

        # zeichne alles!!!
        Szene.zeichne_szenen(self.zeit_unterschied_ms)


    @staticmethod
    def setze_fenster_titel(titel):
        """
        Setzt den Titel für das Fenster.

        :param titel: Der Fenstertitel
        :type titel: str
        """
        pygame.display.set_caption(titel)

    def zeichne_gitter(self, groesse=50, zahlen=True):
        gitter = Gitter(self.breite, self.hoehe, groesse=groesse, zahlen=zahlen)


class VollbildFenster(Fenster):
    def __init__(self, titel="", flags=0, index=0):
        groessen = pygame.display.list_modes()
        w, h = groessen[index]
        print("Verwende Bildschirmgröße: %dx%d", w, h)

        super().__init__(w, h, titel, flags=flags | pygame.FULLSCREEN)
