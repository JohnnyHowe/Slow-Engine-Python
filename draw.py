import pygame
from .geometery import *
from .camera import apply_offset_pos, apply_offset_rect


def game_pos(pos, engine):
    """ Where in the game would the mouse be?
    Args:
        pos (Vector): window position.
        window (window.Window): window object to find window pos for.
    Returns:
        new_pos (Vector): corresponding window position.
    """
    offseted_pos = pos - engine.window.size / 2
    gpos = offseted_pos / engine.window.game_scale
    gpos.y = -gpos.y
    return gpos


def game_size(size, engine):
    """ Convert the display size to game units. """
    return size / engine.window.game_scale


def display_pos(pos, engine):
    """ Where should this game position be displayed?
    Args:
        pos (Vector): game position.
        engine.window (window.Window): window object to find display pos for.
    Returns:
        new_pos (Vector): corresponding display position.
    """
    scaled_pos = pos * engine.window.game_scale
    scaled_pos.y = -scaled_pos.y
    offseted_pos = scaled_pos + engine.window.size / 2
    return offseted_pos


def display_size(size, engine):
    """ Scale up the size for the engine.window
    Args:
        size (Vector): game size.
        engine.window (window.Window): window object to find display size for.
    Returns:
        new_size (Vector): corresponding display size.
    """
    return size * engine.window.game_scale


def display_line(line, engine):
    """ Convert the line game positions to display positions. """
    return Line(display_pos(line.start, engine.window), display_pos(line.end, engine.window))


def display_rect(rect, engine):
    """ Convert the rect game position and size to display units. """
    pos = display_pos(rect.pos(), engine.window)
    size = display_size(rect.size(), engine.window)
    return Rect(pos.x, pos.y, size.x, size.y)


def draw_window_rect(engine, rect, color, width=None):
    """ Draw a rectangle.
    Args:
        engine.window: (window.Window): current window object.
        rect (Rect): rectangle in pixels.
        color (tuple): color of rect.
    """
    if rect_on_screen(rect, engine):
        py_rect = tuple(rect.pos() - rect.size() / 2) + tuple(rect.size())
        if width:
            pygame.draw.rect(engine.window.window, color, py_rect, width)
        else:
            pygame.draw.rect(engine.window.window, color, py_rect)


def draw_game_rect(engine, rect, color, width=None):
    """ Draw a rectangle.
    Args:
        engine.window: (window.Window): current window object.
        rect (Rect): rectangle in game units.
        color (tuple): color of rect.
    """
    moved_rect = apply_offset_rect(engine.camera, rect)
    draw_window_rect(engine, display_rect(moved_rect, engine), color, width=width)


def draw_window_line(engine, line, width, color):
    pygame.draw.line(engine.window.window, color, tuple(line.start), tuple(line.end), width)


def draw_game_line(engine, line, width, color):
    moved_start = apply_offset_pos(engine.camera, line.start)
    moved_end = apply_offset_pos(engine.camera, line.end)
    line = Line(display_pos(moved_start, engine), display_pos(moved_end, engine))
    draw_window_line(engine, line, width, color)


def draw_window_circle(engine, pos, radius, color):
    pygame.draw.circle(engine.window.window, color, tuple(round(pos)), int(radius))


def draw_game_circle(engine, pos, radius, color):
    moved_pos = apply_offset_pos(engine.camera, pos)
    draw_window_circle(engine, display_pos(moved_pos, engine), radius * engine.window.game_scale, color)


def draw_grid(engine, xy_max=5, line_color=(200, 200, 200)):
    num_lines = (xy_max + 1) * 2
    lines = []
    for i in range(1, num_lines):
        lines.append(Line(Vector(i - num_lines // 2, -num_lines // 2), Vector(i - num_lines // 2, num_lines // 2)))
        lines.append(Line(Vector(-num_lines // 2, i - num_lines // 2), Vector(num_lines // 2, i - num_lines // 2)))
    for line in lines:
        draw_game_line(engine, line, 1, line_color)


def rect_on_screen(disp_rect, engine):
    for pos in disp_rect.corners():
        if not pos_on_screen(pos, engine.window):
            return False
    return True


def pos_on_screen(disp_pos, engine):
    """ Is the pos on the screen. """
    return 0 <= disp_pos.x <= engine.window.size.x and 0 <= disp_pos.y <= window.size.y