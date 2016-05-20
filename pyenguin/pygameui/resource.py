import logging
import weakref

import pkg_resources
import pygame

logger = logging.getLogger(__name__)

font_cache = weakref.WeakValueDictionary()

package_name = 'pyenguin'


def get_font(size, use_bold=False):
    filename = 'regular'
    if use_bold:
        filename = 'bold'
    key = '%s:%d' % (filename, size)
    try:
        font = font_cache[key]
    except KeyError:

        backup_fonts = 'helvetica,arial'
        font = pygame.font.SysFont(backup_fonts, size, use_bold)
        font_cache[key] = font

    return font


def scale_image(image, size):
    return pygame.transform.smoothscale(image, size)

