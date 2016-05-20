import pygame

__author__ = 'Mark Weinreuter'


class MausZeiger:
    cursor_m_strings = (  # sized 24x16
        "                ",
        "                ",
        "                ",
        " XXX        XXX ",
        " X..X      X..X ",
        " X...X    X...X ",
        " X.XX.X  X.XX.X ",
        " X.X X.XX.X X.X ",
        " X.X  X..X  X.X ",
        " X.X   XX   X.X ",
        " X.X        X.X ",
        " X.X        X.X ",
        " XXX        XXX ",
        "                ",
        "                ",
        "                ",

    )

    @staticmethod
    def neu(name, muster, hotspot=(0, 0)):
        #  pygame.mouse.set_cursor((24, 24), (0, 0), curs, mask)
        curs, mask = pygame.cursors.compile(muster)
        width = len(muster[0])
        height = len(muster)

        if width % 8 != 0 or height % 8 != 0:
            print("Die Muster Breite und Höhe muss durch 8 teilbar sein.")
            return

        wh = width * height / 8
        if wh != len(curs) or wh != len(mask):
            print("Es muss gelten: Breite * Höhe / 8 == Länge(Cursordaten)")
            return

        if hotspot is None:
            hotspot = (width // 2, height // 2)

        pygame.mouse.set_cursor((width, height), hotspot, curs, mask)
