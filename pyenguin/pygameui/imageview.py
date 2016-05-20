import pygame

from . import resource
from . import view

SCALE_TO_FILL = 0


class BildAnzeige(view.View):
    """A view for displaying an image.

    The only 'content scaling mode' currently supported is 'scale-to-fill'.

    """

    def __init__(self, frame, img, content_mode=SCALE_TO_FILL):
        """Create an image view from an image.

        frame.topleft

            where to position the view.

        frame.size

            if (0, 0) the frame.size is set to the image's size;
            otherwise, the image is scaled to this size.

        """

        assert img is not None

        if frame is None:
            frame = pygame.Rect((0, 0), img.get_size())
        elif frame.w == 0 and frame.h == 0:
            frame.size = img.get_size()

        view.View.__init__(self, frame)

        self._enabled = False
        self.content_mode = content_mode
        self.image = img

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image

    def layout(self):
        assert self.padding[0] == 0 and self.padding[1] == 0
        if self.content_mode == SCALE_TO_FILL:
            self._image = resource.scale_image(self._image, self.frame.size)
        else:
            assert False, "Unknown content_mode"
        view.View.layout(self)

    def ui_zeichne(self):
        self.surface = self._image

