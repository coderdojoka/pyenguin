from pyenguin.bbox import Bewegbar
from pyenguin.ereignis import EreignisBearbeiter
from pyenguin.tasten import Taste

__author__ = 'Mark Weinreuter'


class Ding(object):
    """
    Kleinstes Ding, das gemalt und aktualisiert werden kann.

    Es gehört zu einer Szene und hat einen eindeutigen Namen.
    """

    ANZAHL = 0

    @classmethod
    def neue_nummer(cls):
        cls.ANZAHL += 1
        return str(cls.ANZAHL)

    def __init__(self, szene, prefix=None):
        if prefix is None:
            prefix = self.__class__.__name__

        self.nummer = Ding.neue_nummer()
        self.name = prefix + self.nummer

        self.szene = szene
        self.sichtbar = True

    def verstecke(self):
        self.sichtbar = False

    def zeige(self):
        self.sichtbar = True

    def aktualisiere(self, dt):
        raise NotImplemented("Muss überschrieben werden!")

    def zeichne(self, flaeche):
        raise NotImplemented("Muss überschrieben werden!")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return isinstance(other, Ding) and self.nummer == other.nummer


class SzenenDing(Ding):
    """
    Kleinste Einheit, die zu einer Szene gehört.

    Diese hat einen Verweis, auf die dazugehörige Szene und ihr Eltern-Ding.
    Das Eltern-Ding kann entweder die Szene sein oder eine beliebige Gruppe dieser Szene.
    """

    def __init__(self, szene=None):
        """

        :param szene: Die Szene, zu der dieses Ding gehört
        :type szene: Szene
        """

        # Falls das Eltern-Ding nicht angegeben wurde, verwenden wir die Fenster-Szene
        if szene is None:
            szene = Szene.fenster_szene

        Ding.__init__(self, szene.szene)

        self.ist_entfernt = False
        """
        Flag, indem gespeichert wird, ob dieses Ding aktuell ein Eltern-Element hat oder nicht.

        :type: bool
        """

        self.szene = szene
        """
        Die Szene zu der dieses Objekt gehört.

        :type: Szene
        """

        # Der Verweis auf eltern_ding wird erst unten mittels .dazu(..) gesetzt
        # Da dieses Ding noch nicht registriert ist

        self.eltern_ding = None
        """
        Die Szene oder Gruppe, in der dieses Element liegt.

        :type: SzenenListe
        """

        # Setzt den Eltern verweis
        szene.initiales_dazu(self)

    def entferne(self):
        self.wird_entfernt()
        self.ist_entfernt = True
        self.eltern_ding.raus(self)

    def wechsle_szene(self, s):
        """

        :param s:
        :type s: szene.Szene
        :return:
        :rtype:
        """

        if not isinstance(s, Szene):
            print("%s muss einen Szene sein" % s)

        if s == self.szene:
            print("Objekt ist schon Teil dieser Szene!")
            return

        # Wir müssen auf die Event-Bindungen achten!!
        s.dazu(self)

    def wechsle_gruppe(self, gruppe):

        if not isinstance(gruppe, Gruppe):
            print("%s muss eine Gruppe sein" % gruppe)
            return

        if gruppe.szene != self.szene:
            print("Dieses Objekte und die Gruppe müssen zur gleichen Szene gehören!")
            return

        if gruppe == self.eltern_ding:
            print("Objekt ist schon Teil dieser Gruppe!")
            return

        # Führt den Wechsel (entfernen und hinzufügen) durch
        gruppe.dazu(self)

    def nach_vorne(self):
        if self.ist_entfernt:
            print("Dieses Ding ist vom seinem Eltern-Ding entfernt worden!")
            return

        self.eltern_ding.kind_dinge.remove(self)
        self.eltern_ding.kind_dinge.append(self)

    def wird_entfernt(self):
        pass

    def wurde_hinzugefuegt(self):
        pass


class BewegbaresSzenenDing(Bewegbar, SzenenDing):
    def __init__(self, breite, hoehe, szene=None):
        Bewegbar.__init__(self, breite, hoehe)
        SzenenDing.__init__(self, szene=szene)
        self.bei_maus_klick = None

    def wird_entfernt(self):
        self.szene.entferne_bei_maus_klick(self)

    def wird_hinzugefuegt(self):
        if self.bei_maus_klick is not None:
            self.szene.registriere_bei_maus_klick(self)

    def setze_bei_maus_klick(self, funktion):
        self.bei_maus_klick = funktion
        self.szene.registriere_bei_maus_klick(self)

    def entferne_bei_maus_klick(self):
        self.bei_maus_klick = None
        self.szene.entferne_bei_maus_klick(self)

    @property
    def abstand_rechts(self):
        return self.szene.breite - self.rechts

    @abstand_rechts.setter
    def abstand_rechts(self, wert):
        self.rechts = self.szene.breite - wert

    @property
    def abstand_links(self):
        return self.links

    @abstand_links.setter
    def abstand_links(self, wert):
        self.links = wert

    @property
    def abstand_unten(self):
        return self.szene.hoehe - self.unten

    @abstand_unten.setter
    def abstand_unten(self, wert):
        self.unten = self.szene.hoehe - wert

    @property
    def abstand_oben(self):
        return self.oben

    @abstand_oben.setter
    def abstand_oben(self, wert):
        self.oben = wert

    def zentriere(self):
        self.setze_position(self.szene.breite / 2, self.szene.hoehe / 2)

    def zentriere_breite(self):
        self.x = self.szene.breite / 2

    def zentriere_hoehe(self):
        self.y = self.szene.hoehe / 2

    def raus_links(self):
        return self.welt_x_off + self.links < 0

    def ist_rechts_raus(self):
        return self.welt_x_off + self.rechts > self.szene.breite

    def ist_oben_raus(self):
        return self.welt_y_off + self.oben < 0

    def ist_unten_raus(self):
        return self.welt_y_off + self.unten > self.szene.hoehe

    def ist_raus(self):
        return self.raus_links() or self.ist_rechts_raus() or self.ist_oben_raus() or self.ist_unten_raus()

    def ist_linksrechts_raus(self):
        return self.raus_links() or self.ist_rechts_raus()

    def ist_obenunten_raus(self):
        return self.ist_oben_raus() or self.ist_unten_raus()

    def __str__(self):
        return self.name + ": Pos(Welt-Pos): %d(%d), %d(%d), %dx%d" % (self._x, self.welt_x_off, self._y, self.welt_y_off, self.width, self.height)

    def __eq__(self, other):
        return isinstance(other, BewegbaresSzenenDing) and self.nummer == other.nummer

class SzenenListe(SzenenDing):
    def __init__(self, szene=None):
        SzenenDing.__init__(self, szene)

        self.kind_dinge = []
        """
        Die Kind-Dinge, die zu diesem Ding gehören.

        :type: list[BewegbaresSzenenDing]
        """

        self.anzahl = 0
        """
        Die Anzahl an Kind-Dingen. Sollte das gleiche sein wie: `len(self.kind_dinge)`.

        """

    def dazu(self, ding):
        """
        Fügt das übergebene Ding in die Liste hinzu, falls dies erlaubt ist.

        Außerdem wird das Ding  on seinem vorherigen Eltern-Ding entfernt.
        Die Szene wird auf die Szene des neuen Eltern-Dings gesetzt.

        :param ding:
        :type ding:
        :return:
        :rtype:
        """

        if not isinstance(ding, BewegbaresSzenenDing):
            print("%s kann nicht hinzufügt werden!" % str(ding))
            return

        alte_liste = ding.eltern_ding
        if alte_liste is not None:
            alte_liste.raus(ding)

        self.kind_dinge.append(ding)
        self.anzahl += 1

        # TODO!!!
        # Das ist etwas dumm, da diese Klasse kein Szenending ist...
        ding.eltern_ding = self
        ding.szene = self.szene
        ding.wurde_hinzugefuegt()

    def initiales_dazu(self, ding):
        if isinstance(ding, Szene):
            return

        if not isinstance(ding, BewegbaresSzenenDing):
            print("%s kann nicht hinzufügt werden!" % str(ding))
            return

        self.kind_dinge.append(ding)
        ding.eltern_ding = self
        ding.szene = self.szene

    def raus(self, ding):
        """
        Entfernt das übergebene Ding aus der Liste, der Kind-Dinge,
        falls das Ding in der Liste enthalten war.

        :param ding: Das Ding, das entfernt werden soll
        :type ding: BewegbaresSzenenDing
        :return:
        :rtype:
        """
        if ding in self.kind_dinge:
            ding.wird_entfernt()
            self.kind_dinge.remove(ding)
            self.anzahl -= 1
        else:
            print("%s ist nicht in %s und kann deshalb nicht entfernt werden!" % (str(ding), str(self)))


class Gruppe(BewegbaresSzenenDing, SzenenListe):
    """
    Eine Gruppe dient dazu eine Menge von Dingen zu gruppieren.

    Achtung! Eine Gruppe hat keine Ausdehnung. D.h. eine Gruppe hat immer die
    Breite und Höhe 0!

    """

    def __init__(self, szene=None):
        BewegbaresSzenenDing.__init__(self, 0, 0, szene=szene)
        SzenenListe.__init__(self, szene)

    def entferne(self):
        # Alle Kinder entfernen
        for kind in self.kind_dinge:
            kind.entferne()

        super().entferne()

    def aktualisiere(self, dt):
        super().aktualisiere(dt)

        x_off = self.welt_x_off + self._x
        y_off = self.welt_y_off + self._y

        for element in self.kind_dinge:
            element.welt_x_off = x_off
            element.welt_y_off = y_off
            element.aktualisiere(dt)

    def zeichne(self, flaeche):
        if not self.sichtbar:
            return

        for element in self.kind_dinge:
            if element.sichtbar and not element.ist_raus():
                element.zeichne(flaeche)


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

    fenster_szene = top
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

    def __init__(self, breite, hoehe, pyg_flaeche=None, transparent=False, farbe=None):
        # Benötigt, damit kein Unterschied zwischen Gruppen und Szenen
        self.szene = self
        SzenenListe.__init__(self, self)

        self.x = 0
        self.y = 0
        # self.position = (self.x, self.y)
        self.breite = breite
        self.hoehe = hoehe

        self.farbe = farbe

        self.aktualisierbare_dinge = []

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

        self._aktualisiere = EreignisBearbeiter()

        # Die Szene selbst zeichnet auf einer Fläche, die auf das Fenster gezeichnet wird.
        from pyenguin.flaeche import Leinwand
        self.flaeche = Leinwand(breite, hoehe, pyg_flaeche, transparent)

        # globale Szenen liste
        Szene.szenen.append(self)

    def registriere_bei_maus_klick(self, was):
        if isinstance(was, BewegbaresSzenenDing):
            self._maus_klick_dinge.append(was)
        else:
            print("Kann %s nicht zu den Mausklick-Elementen hinzufügen!" % str(was))

    def entferne_bei_maus_klick(self, was):
        if was in self._maus_klick_dinge:
            self._maus_klick_dinge.remove(was)

    def __del__(self):
        if self != Szene.fenster_szene:
            if self in Szene.szenen:
                Szene.szenen.remove(self)

    def aktualisiere(self, dt):
        self._aktualisiere(dt)
        # TODO: update aktualisieren

    def zeichne(self, dt):
        if not self.sichtbar:
            return

        self.zeichne_alles(dt)
        Szene.fenster_szene.flaeche.blit(self.flaeche, (self.x, self.y))

    def zeichne_alles(self, dt):
        if self.farbe is not None:
            self.flaeche.fuelle(self.farbe)

        for ele in self.kind_dinge:
            ele.aktualisiere(dt)
            if ele.sichtbar:
                ele.zeichne(self.flaeche)

    def mache_aktiv(self):
        Szene.setze_aktive_szene(self)

    def ist_aktiv(self):
        return self == Szene.aktive_szene

    def wurde_aktiv(self):
        pass

    def wurde_inaktiv(self):
        pass

    @classmethod
    def zeichne_szenen(cls, dt):
        cls.fenster_szene.aktualisiere(dt)
        cls.fenster_szene.zeichne_alles(dt)

        for szene in cls.szenen:
            szene.aktualisiere(dt)
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
        :return: Die Szene mit den Koordinaten oder die Fenster-Szene
        :rtype:
        """
        for s in cls.szenen:
            from pyenguin.gitter import Gitter
            if not isinstance(s, Gitter) and s.punkt_innerhalb(x, y) and s.sichtbar:
                return s
        return Szene.fenster_szene

    def verstecke(self):
        super().verstecke()
        Szene.setze_aktive_szene(Szene.fenster_szene)

    def zeige(self):
        super().zeige()
        self.mache_aktiv()

    @classmethod
    def verarbeite_maus_bewegt(cls, ereignis):
        szene = cls.finde_szene(ereignis.pos[0], ereignis.pos[1])
        szene._maus_bewegt(ereignis.pos[0] - szene.x, ereignis.pos[1] - szene.y, ereignis)

        # TODO: warum die erste bedinung??
        if Szene.aktive_szene == Szene.fenster_szene or Szene.aktive_szene.ereignis_weiterleiten:
            Szene.fenster_szene._maus_bewegt(ereignis.pos[0], ereignis.pos[1], ereignis)

    @classmethod
    def verarbeite_maus_geklickt(cls, ereignis):
        Szene.aktive_szene = cls.finde_szene(ereignis.pos[0], ereignis.pos[1])
        sx = ereignis.pos[0] - Szene.aktive_szene.x
        sy = ereignis.pos[1] - Szene.aktive_szene.y

        # Das Klick-Ereignis an alle aktiven Dinge weiterleiten
        for ele in Szene.aktive_szene._maus_klick_dinge:
            if ele.punkt_innerhalb(sx, sy):
                ele.bei_maus_klick(sx, sy, ereignis)

        Szene.aktive_szene._maus_geklickt(sx, sy, ereignis)

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
        Entfernt eine Funktion, die ausgeführt wird, wenn eine Maus-Taste gedrückt wird.
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

    def entferne_maus_losgelassen(self, funktion):
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

    def registriere_aktualisiere(self, funktion):
        """
        Setzt die Funktion, die einmal pro Update-Durchlauf aufgerufen wird,
        in der Dinge aktualisiert werden können.

        :param funktion: die Aktualisierungsfunktion
        :type funktion: (float) -> None
        """
        self._aktualisiere.registriere(funktion)

    def entferne_aktualisiere(self, funktion):
        """
        Entfernt die angegebene Aktualisierugsfunktion.

        :param funktion: Die Funktion, die entfernt werden soll.
        :type funktion: (object) -> None
        """
        self._aktualisiere.entferne(funktion)

    def punkt_innerhalb(self, x, y):
        links = (self.x <= x <= (self.x + self.breite))
        oben = (self.y <= y <= (self.y + self.hoehe))

        return links and oben

    @classmethod
    def setze_aktive_szene(cls, szene):
        cls.aktive_szene.wurde_inaktiv()
        cls.aktive_szene = szene
        cls.aktive_szene.wurde_aktiv()


if __name__ == "__main__":
    import pygame

    pygame.display.init()
    pyg = pygame.display.set_mode((200, 200))
    Szene.fenster_szene = Szene(200, 200, pyg)
    b = BewegbaresSzenenDing(10, 10)
    b2 = BewegbaresSzenenDing(50, 50)
    b2.x = 100
    b2.y = -30

    print(b)

    b._x_bewegung = 10
    b.name = "Box"
    print(b)
