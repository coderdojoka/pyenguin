__author__ = 'Mark Weinreuter'

class Resource:
    def __init__(self):
        pass

SPIELER_S1_STEHEN = "spieler/p1_stand.png"


PAKET_NAMEN = list(filter(lambda s: s[0] != '_', globals().keys()))
