from pyenguin.dinge import SzenenListe, BewegbaresSzenenDing
from pyenguin.ereignis import EreignisBearbeiter
from pyenguin.objekte import Bemalbar
from pyenguin.tasten import Taste

__author__ = 'Mark Weinreuter'


class TopLevel:
    def __init__(self):
        pass

    def __str__(self):
        return "TopLevel"

    def dazu(self, was):
        pass


top = TopLevel()


class Szene(SzenenListe):
    """
    Eine Szene stellt einen Ausschnitt des Fensters da.
    Ein normales Program hat nur eine Szene, die das ganze Fenster füllt.
    Szenen sind Container für Flächen und Gruppen, die innerhalb einer Szene gezeichnet werden.
    Die Position von Kind-Objekte einer Szene ist relativ zur Szenen-position.

    Maus und Tastaturereignisse werden immer an die aktive Szene geleitet!
    """

    aktive_szene = None
    """
    Die aktuell aktive Szene.

    :type: Szene
    """

    fenster_szene = None
    """
    Die ZeichenFlaeche des Spiels (Fensters). Diese wird am Anfang einmal gesetzt.

    :type: Szene
    """

    szenen = []
    """
    :type: list[Szene]
    """

    @classmethod
    def init(cls, szene):
        Szene.fenster_szene = szene
        Szene.szenen.remove(szene)
        Szene.aktive_szene = szene

        # Die Fensterszene leitet nichts weiter
        szene.ereignis_weiterleiten = False

    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=False, farbe=None, elter=None):
        SzenenListe.__init__(self, elter=top)

        self.x = 0
        self.y = 0
        # self.position = (self.x, self.y)
        self.breite = breite
        self.hoehe = hoehe

        # Die Szene selbst zeichnet auf einer Fläche, die auf das Fenster gezeichnet wird.
        self.flaeche = Bemalbar(breite, hoehe, pyg_flaeche, transparent)
        self.farbe = farbe

        self.ereignis_weiterleiten = True
        self._alle_tasten_bearbeiter = EreignisBearbeiter()

        """
        Wird aufgerufen, falls eine beliebige Tasten gedrückt wird.

        :type: pyenguin.EreignisBearbeiter
        """

        self._maus_klick_dinge = []
        """
        Die Liste der Maus aktiven Flächen.

        :type: list[pyenguin.BewegbaresSzenenDing]
        """

        self._tasten = {}
        """
        Tastendruck-Funktionen werden hier gespeichert.

        :type: dict[int, pyenguin.Taste]
        """

        self._maus_geklickt = EreignisBearbeiter()
        self._maus_losgelassen = EreignisBearbeiter()
        self._maus_bewegt = EreignisBearbeiter()

        # Benötigt, damit kein Unterschied zwischen Gruppen und Szenen
        self.szene = self

        # globale Szenen liste
        Szene.szenen.append(self)

    def neues_maus_klick_ding(self, was):
        if isinstance(was, BewegbaresSzenenDing):
            self._maus_klick_dinge.append(was)
        else:
            print("Kann %s nicht zu den Mausklickelement hinzufügen!" % str(was))

    def entferne_maus_klick_ding(self, was):
        if was in self._maus_klick_dinge:
            self._maus_klick_dinge.remove(was)

    def raus(self, was):
        SzenenListe.raus(self, was)
        self.entferne_maus_klick_ding(was)

    def dazu(self, was):
        SzenenListe.dazu(self, was)
        if was.bei_maus_klick is not None:
            self.neues_maus_klick_ding(was)

    def __del__(self):
        if self != Szene.fenster_szene:
            Szene.szenen.remove(self)

    def zeichne(self, dt):
        self.zeichne_alles(dt)
        Szene.fenster_szene.flaeche.blit(self.flaeche, (self.x, self.y))

    def zeichne_alles(self, dt):
        if self.farbe is not None:
            self.flaeche.fuelle(self.farbe)

        for ele in self.kind_elemente:
            ele.aktualisiere(dt)
            if ele.sichtbar:
                ele.zeichne(self.flaeche)

    def fokusiere(self):
        Szene.aktive_szene = self

    @classmethod
    def zeichne_szenen(cls, dt):
        cls.fenster_szene.zeichne_alles(dt)

        for szene in cls.szenen:
            szene.zeichne(dt)

    @classmethod
    def verarbeite_taste_unten(cls, ereignis):
        Szene.aktive_szene._taste_unten(ereignis)
        if Szene.aktive_szene.ereignis_weiterleiten:
            Szene.fenster_szene._taste_unten(ereignis)

    @classmethod
    def verarbeite_taste_oben(cls, ereignis):
        Szene.aktive_szene._taste_oben(ereignis)
        if Szene.aktive_szene.ereignis_weiterleiten:
            Szene.fenster_szene._taste_oben(ereignis)

    @classmethod
    def finde_szene(cls, x, y):
        """
        Sucht die Szene, die die angegeben Koordinaten enthält.

        :param x:
        :type x:
        :param y:
        :type y:
        :return: Die Szene mit den Koordinaten oder die Fensterszene
        :rtype:
        """
        for s in cls.szenen:
            if s.punkt_innerhalb(x, y):
                return s
        return Szene.fenster_szene

    @classmethod
    def verarbeite_maus_bewegt(cls, ereignis):
        szene = cls.finde_szene(ereignis.pos[0], ereignis.pos[1])
        szene._maus_bewegt(ereignis.pos[0] - szene.x, ereignis.pos[1] - szene.y, ereignis)

        if Szene.aktive_szene == Szene.fenster_szene or Szene.aktive_szene.ereignis_weiterleiten:
            Szene.fenster_szene._maus_bewegt(ereignis.pos[0], ereignis.pos[1], ereignis)

    @classmethod
    def verarbeite_maus_geklickt(cls, ereignis):
        Szene.aktive_szene = cls.finde_szene(ereignis.pos[0], ereignis.pos[1])
        sx = ereignis.pos[0] - Szene.aktive_szene.x
        sy = ereignis.pos[1] - Szene.aktive_szene.y
        Szene.aktive_szene._maus_geklickt(sx, sy, ereignis)

        # Das Klickereignis an alle aktiven Flächen weiterleiten
        for ele in Szene.aktive_szene._maus_klick_dinge:
            if ele.punkt_innerhalb(sx, sy):
                ele.bei_maus_klick(sx, sy, ereignis)

        if Szene.aktive_szene.ereignis_weiterleiten:
            Szene.fenster_szene._maus_geklickt(ereignis.pos[0], ereignis.pos[1], ereignis)

    @classmethod
    def verarbeite_maus_losgelassen(cls, ereignis):
        szene = cls.finde_szene(ereignis.pos[0], ereignis.pos[1])
        szene._maus_losgelassen(ereignis.pos[0] - szene.x, ereignis.pos[1] - szene.y, ereignis)

        if Szene.aktive_szene.ereignis_weiterleiten:
            Szene.fenster_szene._maus_losgelassen(ereignis.pos[0], ereignis.pos[1], ereignis)

    def _taste_oben(self, ereignis):
        # allgemeiner Bearbeiter
        self._alle_tasten_bearbeiter(False, ereignis.key)

        # spezialisierter Handler
        if ereignis.key in self._tasten:
            taste = self._tasten[ereignis.key]
            taste.wenn_oben(ereignis)

        # Taste gedrückt
        # allgemeiner Bearbeiter
        self._alle_tasten_bearbeiter(True, ereignis)

    def _taste_unten(self, ereignis):

        self._alle_tasten_bearbeiter(True, ereignis.key, ereignis.unicode)

        # spezialisierter Handler
        if ereignis.key not in self._tasten:
            # Lazy add keys
            self._tasten[ereignis.key] = Taste(ereignis.key, ereignis.unicode)

        taste = self._tasten[ereignis.key]
        taste.wenn_unten(taste)

    def registriere_alle_tasten(self, funktion):
        """
        Die Funktion wird aufgerufen, wenn eine beliebige Taste gedrückt wird

        :param funktion:
        :type funktion: (bool, str, int) -> None
        """
        self._alle_tasten_bearbeiter.registriere(funktion)

    def entferne_alle_tasten(self, funktion):
        """
        Entfernt die Funktion wird aufgerufen, wenn eine beliebige Taste gedrückt wird

        :param funktion:
        :type funktion: (bool, Str, int) -> None
        """
        self._alle_tasten_bearbeiter.entferne(funktion)

    def registriere_taste_oben(self, taste, funktion):
        """
        Registriert eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt und losgelassen wird.

        :param taste: die Taste z.B. die a-Taste ist 97. Die wichtigsten Tasten sind vordefiniert, so entspricht T_a der 'a'-Taste
        :type taste: int
        :param funktion: Die Funktion die aufgerufen wird. Sie muss 2 Parameter akzeptieren, der
        Erste gibt an, ob die Taste gedrückt oder losgelassen ist und der Zweite ist das Event Objekt
        :type funktion: (bool, pyenguin.Taste) -> None
        """
        if taste not in self._tasten:
            self._tasten[taste] = Taste(taste)

        self._tasten[taste].wenn_oben.registriere(funktion)

    def entferne_taste_oben(self, taste, funktion):
        """
        Entfernt eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt und losgelassen wird.

        :param taste: die Taste
        :type taste: int
        :param funktion: Die Funktion die aufgerufen wird.
        :type funktion: (Taste) -> None
        """
        if taste in self._tasten:
            self._tasten[taste].wenn_oben.entferne(funktion)

    def registriere_taste_unten(self, taste, funktion):
        """
        Registriert eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt wird.

        :param taste: die Taste z.B. die a-Taste ist 97. Die wichtigsten Tasten sind vordefiniert, so entspricht T_a der 'a'-Taste
        :type taste: int
        :param funktion: Die Funktion die aufgerufen wird. Sie muss 1 Parameter akzeptieren
        :type funktion: (Zeichen) -> None
        """
        if taste not in self._tasten:
            self._tasten[taste] = Taste(taste)

        self._tasten[taste].wenn_unten.registriere(funktion)

    def entferne_taste_unten(self, taste, funktion):
        """
        Entfernt eine Funktion, die ausgeführt wird, wenn die angegebene Taste runter gedrückt wird.

        :param taste: die Taste
        :type taste: int
        :param funktion: Die Funktion die aufgerufen wird.
        :type funktion: (Taste) -> None
        """
        if taste in self._tasten:
            self._tasten[taste].wenn_unten.entferne(funktion)

    def registriere_maus_bewegt(self, funktion):
        """
        Registriert eine Funktion, die ausgeführt wird, wenn eine Maus-Taste gedrückt wird.
        Wenn die Funktion aufgerufen wird, wird ihr ein Objekt übergeben, das so aufgebaut ist:

            button: 1-3 # welche Taste: 1 = Links, ...
            pos: (x,y) # Tupel mit der Position

        :param funktion: Die Funktion die aufgerufen werden soll, wenn eine Taste gedrückt wurde
        :type funktion: (object) -> None
        """
        self._maus_bewegt.registriere(funktion)

    def entferne_maus_bewegt(self, funktion):
        """
        Enfternt eine Funktion, die ausgeführt wird, wenn eine Maus-Taste gedrückt wird.
        Wenn die Funktion aufgerufen wird, wird ihr ein Objekt übergeben, das so aufgebaut ist:

            button: 1-3 # welche Taste: 1 = Links, ...
            pos: (x,y) # Tupel mit der Position

        :param funktion: Die Funktion die aufgerufen werden soll, wenn eine Taste gedrückt wurde
        :type funktion: (object) -> None
        """
        self._maus_bewegt.entferne(funktion)

    def registriere_maus_losgelassen(self, funktion):
        """
        Registriert eine Funktion, die aufgerufen wird, wenn eine Maustaste losgelassen wird.

        :param funktion: Die Funktion
        :type funktion: (object)->None
        """
        self._maus_losgelassen.registriere(funktion)

    def entferene_maus_losgelassen(self, funktion):
        """
        Entfernt eine Funktion, die aufgerufen wird, wenn eine Maustaste losgelassen wird.

        :param funktion: Die Funktion
        :type funktion: (object)->None
        """
        self._maus_losgelassen.entferne(funktion)

    def registriere_maus_geklickt(self, funktion):
        """
        Registriert eine Funktion, die aufgerufen wird, wenn eine Maustaste gedrückt wird.

        :param funktion:
        :type funktion: (object)->None
        """
        self._maus_geklickt.registriere(funktion)

    def entferne_maus_geklickt(self, funktion):
        """
        Entfernt eine Funktion, die aufgerufen wird, wenn eine Maustaste gedrückt wird.

        :param funktion:
        :type funktion: (object)->None
        """
        self._maus_geklickt.entferne(funktion)

    def punkt_innerhalb(self, x, y):
        left = (self.x <= x <= (self.x + self.breite))
        top = (self.y <= y <= (self.y + self.hoehe))

        return left and top
