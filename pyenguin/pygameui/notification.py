import pygame

from . import dialog
from . import label

DOWN = 0
UP = 1
IDLE = 2


class NotificationView(dialog.DialogView):
    """A notification alert view.

    The notification animates down from the top of
    the window and can be closed by mouse clock or
    automatically close itself after a few seconds.

    auto_close

        Automatically close the notification;
        default: True.

    auto_close_after

        How long to wait before closing the notification;
        default: 3 (seconds).

    """

    def __init__(self, msg):
        from pyenguin.pygameui.gui_szene import GuiSzene
        frame = pygame.Rect(0, 0, GuiSzene.aktiv.breite//3, GuiSzene.aktiv.hoehe//2)
        dialog.DialogView.__init__(self, frame)

        self.message_label = label.Label(pygame.Rect((0, 0), frame.size),
                                         msg, wrap=label.WORD_WRAP)
        self.add_child(self.message_label)

        self.auto_close = True
        self.auto_close_after = 100
        self.elapsed = 0

    def layout(self):
        assert self.get_border_widths()[0] == 0  # top; check for animations
        assert self.padding[0] == 0 and self.padding[1] == 0
        self.message_label.shrink_wrap()
        self.message_label.frame.w = self.frame.w
        self.frame.h = self.message_label.frame.h
        dialog.DialogView.layout(self)

    def parented(self):
        self.animation_state = DOWN
        self.frame.top = -self.frame.h
        self.frame.centerx = self.parent.frame.w // 2
        self.stylize()

    def maus_unten(self, button, point):
        dialog.DialogView.maus_unten(self, button, point)
        self.animation_state = UP

    def ui_aktualisiere(self, dt):
        dialog.DialogView.ui_aktualisiere(self, dt)
        rate = 30
        if self.animation_state == DOWN:
            if self.frame.top < 0:
                self.frame.top += dt * rate
                self.frame.top = min(self.frame.top, 0)
            else:
                self.animation_state = IDLE
        elif self.animation_state == UP:
            if self.frame.top > -self.frame.h:
                self.frame.top -= dt * rate
            else:
                self.rm()
        elif self.animation_state == IDLE:
            self.elapsed += dt
            if self.elapsed > self.auto_close_after:
                self.animation_state = UP


def show_notification(message):
    notification = NotificationView(message)
    from .gui_szene import GuiSzene
    GuiSzene.aktiv.add_child(notification)
    notification.stylize()
