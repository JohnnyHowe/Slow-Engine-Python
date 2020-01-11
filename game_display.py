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


def game_size(size, window):
    """ Convert the display size to game units. """
    return size / window.game_scale


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


def display_line(line, window):
    """ Convert the line game positions to display positions. """
    return Line(display_pos(line.start, window), display_pos(line.end, window))


def display_rect(rect, window):
    """ Convert the rect game position and size to display units. """
    pos = display_pos(rect.pos(), window)
    size = display_size(rect.size(), window)
    return Rect(pos.x, pos.y, size.x, size.y)


def draw_rect(window, rect, color, width=None):
    """ Draw a rectangle.

    Args:
        window: (window.Window): current window object.
        rect (Rect): rectangle in pixels.
        color (tuple): color of rect.
    """
    if rect_on_screen(rect, window):
        py_rect = tuple(rect.pos() - rect.size() / 2) + tuple(rect.size())
        if width:
            pygame.draw.rect(window.window, color, py_rect, width)
        else:
            pygame.draw.rect(window.window, color, py_rect)


def draw_game_rect(window, rect, color, width=None):
    """ Draw a rectangle.

    Args:
        window: (window.Window): current window object.
        rect (Rect): rectangle in game units.
        color (tuple): color of rect.
    """
    draw_rect(window, display_rect(rect, window), color, width=width)


def draw_line(window, line, width, color):
    pygame.draw.line(window.window, color, tuple(line.start), tuple(line.end), width)


def draw_game_line(window, line, width, color):
    display_line = Line(display_pos(line.start, window), display_pos(line.end, window))
    draw_line(window, display_line, width, color)


def draw_circle(window, pos, radius, color):
    pygame.draw.circle(window.window, color, tuple(round(pos)), int(radius))


def draw_game_circle(window, pos, radius, color):
    draw_circle(window, display_pos(pos, window), radius * window.game_scale, color)


def rect_on_screen(disp_rect, window):
    for pos in disp_rect.corners():
        if not pos_on_screen(pos, window):
            return False
    return True


def pos_on_screen(disp_pos, window):
    """ Is the pos on the screen. """
    return 0 <= disp_pos.x <= window.size.x and 0 <= disp_pos.y <= window.size.y
