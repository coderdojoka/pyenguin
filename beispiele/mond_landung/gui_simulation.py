import math

from pyenguin import BildSpeicher
from pyenguin import Gruppe
from simulation import Mond, Planet, Rakete, Simulation, Vektor2

__author__ = 'Mark Weinreuter'


class GSimulation(Simulation):
    def __init__(self, planet, mond):
        super().__init__(planet, mond)
        self.gruppe = Gruppe()
        self.gruppe.dazu(planet.bild)
        self.gruppe.dazu(mond.bild)

    def neue_grakete(self, geschwindigkeit, winkel):

        rakete = GRakete()
        rakete.position.y = -self.planet.radius - rakete.radius
        winkel = winkel / 360 * 2 * math.pi
        rakete.geschwindigkeit = Vektor2(math.sin(winkel) * geschwindigkeit, -math.cos(winkel) * geschwindigkeit)

        if super().neue_rakete(rakete):
            self.gruppe.dazu(rakete.bild)

    def naechster_schritt(self):
        super().naechster_schritt()
        self.mond.position_anpassen()
        for rakete in self.raketen:
            rakete.position_anpassen()


class GMond(Mond):
    def __init__(self, masse, abstand, winkel_geschwindigkeit=1):
        self.bild = BildSpeicher.gib("mond")
        super().__init__(masse, self.bild.halbe_hoehe, abstand, winkel_geschwindigkeit)

    def position_anpassen(self):
        self.bild.setze_position(self.position.x, self.position.y)


class GPlanet(Planet):
    def __init__(self, masse):
        self.bild = BildSpeicher.gib("planet")
        super().__init__(masse, self.bild.halbe_hoehe)

        self.bild.setze_position(0, 0)


class GRakete(Rakete):
    def __init__(self, masse=10):
        self.bild = BildSpeicher.gib("rakete")
        super().__init__(masse, self.bild.halbe_hoehe)

    def position_anpassen(self):
        # Wir haben nicht bei mathematisch 0° angefangen sondern bei 270(-90)
        self.bild.setze_rotation(180 / math.pi * math.atan2(-self.geschwindigkeit.y, self.geschwindigkeit.x) - 90)
        self.bild.setze_position(self.position.x, self.position.y)
