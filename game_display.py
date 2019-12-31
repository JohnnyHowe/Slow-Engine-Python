import pygame
from .geometery import *


def game_pos(pos, window):
    """ Where in the game would the mouse be?

    Args:
        pos (Vector): window position.
        window (window.Window): window object to find window pos for.

    Returns:
        new_pos (Vector): corresponding window position.
    """
    offseted_pos = pos - window.size / 2
    gpos = offseted_pos / window.game_scale
    gpos.y = -gpos.y
    return gpos


def display_pos(pos, window):
    """ Where should this game position be displayed?

    Args:
        pos (Vector): game position.
        window (window.Window): window object to find display pos for.

    Returns:
        new_pos (Vector): corresponding display position.
    """
    scaled_pos = pos * window.game_scale
    scaled_pos.y = -scaled_pos.y
    offseted_pos = scaled_pos + window.size / 2
    return offseted_pos


def display_size(size, window):
    """ Scale up the size for the window

    Args:
        size (Vector): game size.
        window (window.Window): window object to find display size for.

    Returns:
        new_size (Vector): corresponding display size.
    """
    return size * window.game_scale


def draw_rect(window, pos, size, color):
    """ Draw a rectangle.

    Args:
        window: (window.Window): current window object.
        pos (Vector): center window position of rectangle.
        size (Vector): window size of rect.
        color (tuple): color of rect.
    """
    rect = tuple(pos - size / 2) + tuple(size)
    pygame.draw.rect(window.window, color, rect)


def draw_game_rect(window, pos, size, color):
    """ Draw a rectangle.

    Args:
        window: (window.Window): current window object.
        pos (Vector): center game position of rectangle.
        size (Vector): game size of rect.
        color (tuple): color of rect.
    """
    draw_rect(window, display_pos(pos, window), display_size(size, window), color)
