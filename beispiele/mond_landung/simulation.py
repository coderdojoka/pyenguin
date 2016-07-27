import math

__author__ = 'Mark Weinreuter'


class Vektor2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def abstand(self, vek):
        return math.sqrt((vek.x - self.x) ** 2 + (vek.y - self.y) ** 2)

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __sub__(self, other):
        return Vektor2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vektor2(self.x + other.x, self.y + other.y)

    def normiere(self):
        betrag = abs(self)
        if betrag == 0:
            return

        self.x /= betrag
        self.y /= betrag

        return self

    def skaliere(self, skalar):
        self.x *= skalar
        self.y *= skalar
        return self

    def skaliere_kopie(self, skalar):
        return Vektor2(self.x * skalar, self.y * skalar)

    def __str__(self):
        return "X: %.2f Y: %.2f" % (self.x, self.y)


class SimuObjekt:
    def __init__(self, masse, radius):
        self.masse = masse
        self.radius = radius
        self.position = Vektor2()


class Rakete(SimuObjekt):
    def __init__(self, masse, radius):
        super().__init__(masse, radius)
        self.geschwindigkeit = Vektor2()

    def gravitation(self, dt, planet):
        r = planet.position.abstand(self.position)
        richtung = (planet.position - self.position).normiere()
        kraft = planet.masse * self.masse / r ** 2

        return richtung.skaliere(kraft * dt / self.masse)


class Mond(SimuObjekt):
    def __init__(self, masse, radius, abstand, winkel_geschwindigkeit=1):
        super().__init__(masse, radius)
        self.winkel_geschwindigkeit = winkel_geschwindigkeit
        self.abstand = abstand
        self.winkel = 0

    def bewege(self, dt):
        self.winkel += self.winkel_geschwindigkeit * dt
        self.position.x = math.sin(self.winkel) * self.abstand
        self.position.y = -math.cos(self.winkel) * self.abstand


class Planet(SimuObjekt):
    def __init__(self, masse, radius):
        super().__init__(masse, radius)


class Simulation:
    def __init__(self, planet, mond):
        self.zeit_schritt = .1

        self.planet = planet
        self.mond = mond
        self.raketen = []

    def neue_rakete(self, rakete):

        if rakete not in self.raketen:
            self.raketen.append(rakete)
            return True

        return False

    def naechster_schritt(self):
        self.mond.bewege(self.zeit_schritt)
        print(self.mond.position)
        for rakete in self.raketen:
            delta_geschwindigkeit = rakete.gravitation(self.zeit_schritt, self.planet)
            delta_geschwindigkeit += rakete.gravitation(self.zeit_schritt, self.mond)
            rakete.geschwindigkeit += delta_geschwindigkeit
            rakete.position += rakete.geschwindigkeit.skaliere_kopie(self.zeit_schritt)
