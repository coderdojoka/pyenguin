import logging

from pyenguin.bbox import Box
from pyenguin.szene import Szene

__author__ = 'Mark Weinreuter'

from . import focus
from . import View

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class GuiSzene(View, Szene):
    aktiv = None

    def __init__(self, breite, hoehe, farbe=(255, 255, 255)):
        Szene.__init__(self, breite, hoehe, farbe=farbe)
        View.__init__(self, Box(0, 0, breite, hoehe))

        self.registriere_maus_losgelassen(self.__maus_oben)
        self.registriere_maus_geklickt(self.__maus_unten)
        self.registriere_maus_bewegt(self.__maus_bewegt)

        self.down_in_view = None

        # pygame.key.set_repeat(200, 50)
        # window.rect = pygame.Rect((0, 0), (breite, hoehe))
        GuiSzene.aktiv = self

    def ui_aktualisiere(self, dt):
        View.ui_aktualisiere(self, dt)

    def zeichne(self, dt):
        self.ui_aktualisiere(dt)
        self.ui_zeichne()
        Szene.fenster_szene.flaeche.blit_pyg_flaeche(self.surface, (0, 0))

    def _taste_unten(self, e):
        if focus.view:
            focus.view.taste_unten(e.key, e.unicode)
            bubble_event = False
        else:
            self.taste_unten(e.key, e.unicode)

    def _taste_oben(self, e):

        if focus.view:
            focus.view.taste_oben(e.key)
            bubble_event = False
        else:
            self.taste_oben(e.key)

    def __maus_unten(self, x, y, e):
        hit_view = self.hit(e.pos)
        logger.debug('hit %s' % hit_view)

        if (hit_view is not None and
                not isinstance(hit_view, GuiSzene)):
            focus.set(hit_view)

            self.down_in_view = hit_view
            pt = hit_view.from_window(e.pos)
            hit_view.maus_unten(e.button, pt)

            bubble_event = False

        else:
            focus.set(None)

    def __maus_oben(self, x, y, e):

        hit_view = self.hit(e.pos)

        if hit_view is not None:

            if self.down_in_view and hit_view != self.down_in_view:
                self.down_in_view.blurred()
                focus.set(None)
            pt = hit_view.from_window(e.pos)
            hit_view.maus_hoch(e.button, pt)

            bubble_event = True

        # Reset view
        self.down_in_view = None

    def __maus_bewegt(self, x, y, e):
        if self.down_in_view and self.down_in_view.draggable:
            pt = self.down_in_view.from_window(e.pos)
            self.down_in_view.maus_gezogen(pt, e.rel)

            bubble_event = False
        else:
            self.maus_bewegt(e.pos)

    def reagiere(e):
        down_in_view

        bubble_event = True
        mouse_point = pygame.mouse.get_pos()

        return bubble_event
