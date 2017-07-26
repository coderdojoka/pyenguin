from pygame.constants import *

from pyenguin.ereignis import EreignisBearbeiter

__author__ = 'Mark Weinreuter'


class Taste:
    def __init__(self, pyg_konstante, zeichen=""):
        self.pyg_konstante = pyg_konstante
        self.zeichen = zeichen

        self.wenn_oben = EreignisBearbeiter()
        self.wenn_unten = EreignisBearbeiter()


# Tn-Codes

T_0 = K_0
T_1 = K_1
T_2 = K_2
T_3 = K_3
T_4 = K_4
T_5 = K_5
T_6 = K_6
T_7 = K_7
T_8 = K_8
T_9 = K_9
T_a = K_a
T_b = K_b
T_c = K_c
T_d = K_d
T_e = K_e
T_f = K_f
T_g = K_g
T_h = K_h
T_i = K_i
T_j = K_j
T_k = K_k
T_l = K_l
T_m = K_m
T_n = K_n
T_o = K_o
T_p = K_p
T_q = K_q
T_r = K_r
T_s = K_s
T_t = K_t
T_u = K_u
T_v = K_v
T_w = K_w
T_x = K_x
T_y = K_y
T_z = K_z

T_LEER = K_SPACE
T_ENTER = K_RETURN
T_ESCAPE = K_ESCAPE

# Pfeiltasten
T_UNTEN = K_DOWN
T_RECHTS = K_RIGHT
T_LINKS = K_LEFT
T_OBEN = K_UP

T_ENTFERNEN = K_DELETE
T_ASTERISK = K_ASTERISK
T_BACKSPACE = K_BACKSPACE
T_DOPPELPUNKT = K_COLON
T_KOMMA = K_COMMA

T_LSHIFT = K_LSHIFT
T_RSHIFT = K_LSHIFT

T_FRAGEZEICHEN = K_QUESTION

T_PUNKT = K_PERIOD
T_PLUS = K_PLUS
T_MINUS = K_MINUS

TASTEN_NAMEN = list(filter(lambda s: s[:2] == "T_", globals().keys()))
TASTEN_CODES = {globals()[name]: name for name in TASTEN_NAMEN}
