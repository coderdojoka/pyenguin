class Bild(ZeichenbaresElement):
    def render(self, pyg_zeichen_flaeche, x_off=0, y_off=0):
        pyg_zeichen_flaeche.blit(self.__pygame_bild, (self.x + x_off, self.y + y_off))

    def __init__(self, x, y, bild, eltern_flaeche=None, position_geaendert=lambda: None):
        """
        Ein neues Bild, das gezeichnet wird.

        :param x: die x-Position
        :type x: float
        :param y: die y-Position
        :type y: float
        :param bild: Entweder der Schlüssel für den BilderSpeicher oder eine pygame Surface
        :type bild: str|pygame.Surface
        :param alpha: Wahr, falls das Bild einen Alpha-Kanal hat (Transparenz)
        :type alpha: bool
        """
        if isinstance(bild, str):
            self.__pygame_bild = BildSpeicher.gib_pygame_bild(bild)
        elif isinstance(bild, pygame.Surface):
            self.__pygame_bild = bild
        else:
            raise ValueError("Bitte Schlüssel des Bildes im Bildspeicher angeben.")

        self.__orginal_pygame_surface = self.__pygame_bild
        self.__quelle = bild

        SkalierbaresElement.__init__(self, self)
        ZeichenbaresElement.__init__(self, x, y, self.__pygame_bild.get_width(), self.__pygame_bild.get_height(), farbe=None,
                                     eltern_flaeche=eltern_flaeche,
                                     position_geaendert=position_geaendert)

    def _rotation_skalierung_anwenden(self):
        self.__pygame_bild = pygame.transform.rotozoom(self.__orginal_pygame_surface, self._winkel, self._skalierung)

        # das umgebende Rechteck hat sich geändert => Bild Zentrum anpassen
        rect = self.__pygame_bild.get_rect()
        return rect.width, rect.height

    def klone(self, x, y):
        b = Bild(x, y, self.__quelle, self._eltern_flaeche)
        return b


class BildWechsler(ZeichenbaresElement):
    def __init__(self, x, y, bilder_namen_liste, eltern_flaeche=None, position_geaendert=lambda: None):
        # Candy für Faule
        if isinstance(bilder_namen_liste, str):
            bilder_namen_liste = [bilder_namen_liste]

        self.__name_liste = bilder_namen_liste
        self.__pygame_bilder = []
        self.aktuelles_bild = 0
        self.zeige_erstes_bild = lambda: self.zeige_bild(0)
        self.zeige_letztes_bild = lambda: self.zeige_bild(-1)

        if len(bilder_namen_liste) == 0:
            raise ValueError("Bilder Liste darf nicht leer sein!")

        groesse = (0, 0)
        # alle Bilder laden und Größe ermittlen
        for name in bilder_namen_liste:
            pg_bild = BildSpeicher.gib_pygame_bild(name)
            groesse = max(groesse[0], pg_bild.get_width()), max(groesse[1], pg_bild.get_height())

            self.__pygame_bilder.append(pg_bild)

        self.anzahl_bilder = len(self.__pygame_bilder)

        super().__init__(x, y, *groesse, farbe=None, eltern_flaeche=eltern_flaeche,
                         position_geaendert=position_geaendert)

    def zeige_bild(self, index):
        if index < 0:
            index = 0
        elif index >= self.anzahl_bilder:
            index = self.anzahl_bilder - 1

        self.aktuelles_bild = index

    def naechstes_bild(self):
        if self.aktuelles_bild == self.anzahl_bilder - 1:
            self.aktuelles_bild = 0
        else:
            self.aktuelles_bild += 1

    def vorheriges_bild(self):
        if self.aktuelles_bild == 0:
            self.aktuelles_bild = self.anzahl_bilder - 1
        else:
            self.aktuelles_bild -= 1

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        bild = self.__pygame_bilder[self.aktuelles_bild]
        # Bild zentriert zeichnen
        pyg_zeichen_flaeche.blit(bild, (
            self.x + x_offset + (self.breite - bild.get_width()) / 2,
            self.y + y_offset + (self.hoehe - bild.get_height()) / 2))

    def klone(self, x, y):
        BildWechsler(x, y, self.__name_liste, self._eltern_flaeche)
