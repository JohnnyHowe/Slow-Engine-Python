import pygame

from .vectors import Vector


class Window:
    def __init__(self, game_obj, size):
        """ size (Vector2d): size of window. """
        self.window_size = size
        self.window_scale = 1
        self.window = None
        self.zoom = 1
        self.set_window()
        self.game_obj = game_obj

    def set_window(self):
        self.window = pygame.display.set_mode(tuple(self.window_size))
        self.window_scale = (self.window_size.x / 20) * self.zoom

    def set_zoom(self, zoom):
        self.zoom = zoom
        self.set_window()

    def draw_rect(self, pos, size, color):
        pygame.draw.rect(self.window, color, self.display_rect(pos, size))

    # def draw_circle(self, pos, radius, color):
    #     pygame.draw.circle(self.window, pos, radius, color)

    def draw_line(self, pos1, pos2, width, color):
        pygame.draw.line(self.window, color, self.display_pos(pos1).tuple(), self.display_pos(pos2).tuple(), width)

    def display_pos(self, pos):
        """ pos (Vector2d): game position.
        Return (Vector2d) display position. """
        return Vector(pos.x * self.window_scale + self.window_size.x / 2,
                      -pos.y * self.window_scale + self.window_size.y / 2)

    def real_pos(self, rpos):
        """ Undo display_pos """
        return Vector((rpos.x - self.window_size.x / 2) / self.window_scale,
                      (-(rpos.y - self.window_size.y / 2) / self.window_scale))

    def display_size(self, size):
        """ size (Vector2d): game size.
        Return (Vector2d) display size. """
        return Vector(size.x * self.window_scale, size.y * self.window_scale)

    def display_rect(self, pos, size):
        """ pos (Vector2d): game position.
        size (Vector2d): game size.
        Return (tuple): display rect """
        display_size = self.display_size(size)
        display_pos = self.display_pos(pos)
        display_pos.x -= display_size.x / 2
        display_pos.y -= display_size.y / 2
        return tuple(display_pos) + tuple(display_size)
