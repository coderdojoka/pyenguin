__author__ = 'Mark Weinreuter'

# ein paar vordefinierte Farben
WEISS = (255, 255, 255)
MATT_WEISS = (230, 230, 230)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
MATT_ROT = (220, 0, 20)

GRAU = (70, 70, 70)
HELL_GRAU = (200, 200, 200)
FAST_WEISS = (245, 245, 245)

GRUEN = (0, 255, 0)
HELL_GRUEN = (120, 250, 20)
NEON_GRUEN = (128, 255, 158)
MATT_GRUEN = (97, 195, 120)
GRAU_GRUEN = (80, 140, 80)

BLAU = (0, 0, 255)
GRAU_BLAU = (138, 176, 196)
MATT_BLAU = (125, 191, 225)
ORANGE = (255, 170, 0)
OLIVE = (200, 200, 80)

DUNKEL_LILA = (255, 0, 255)
LILA = (205, 100, 255)
MATT_LILA = (196, 149, 218)
TUERKIS = (0, 255, 255)
GELB = (255, 255, 0)
HELL_GELB = (246, 255, 99)

BRAUN = (190, 140, 45)
MATT_BRAUN = (160, 120, 35)

MATT_GOLD = (210, 183, 34)
GRAU_GOLD = (190, 175, 30)

TRANSPARENT = (255, 255, 255, 255)

FARBEN_NAMEN = list(filter(lambda s: s.isupper(), globals().keys()))

if __name__ == "__main__":
    print(globals())