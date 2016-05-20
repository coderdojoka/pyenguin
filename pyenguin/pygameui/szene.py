from . import focus
from . import view


class Szene2(view.View):
    """A view that takes up the entire window content area."""

    def __init__(self, mit_hintergrund=True):
        view.View.__init__(self, window.rect)
        self._mit_hintergrund = mit_hintergrund

    def taste_unten(self, key, code):
        from . import pygame

        if key == pygame.K_ESCAPE:
            weg()

    def deaktiviere(self):
        pass

    def aktiviere(self):
        self.stylize()

        if self._mit_hintergrund:
            # Keine Hintergrundfarbe zulassen, da sonst eine Mischung aus Spiel und GUI
            # nicht möglich wäre, um allerdings dropshadows zu erlauben
            # überzeichnen wir den Hintergrund mit einem transparenten Schwarz
            self.background_color = (0, 0, 0, 0)

    def ui_zeichne(self):
        super().ui_zeichne()
