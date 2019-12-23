import pygame

from .vectors import Vector
from .coordinate_geometry import Line


class Window:
    def __init__(self, game_obj, size):
        """ size (Vector2d): size of window. """
        self.window_size = size
        self.window_scale = None
        self.window = None
        self.zoom = 1
        self.set_window()
        self.game_obj = game_obj

    def set_window(self):
        self.window = pygame.display.set_mode(tuple(self.window_size), pygame.RESIZABLE)
        self.window_scale = (min(self.window_size) / 20) * self.zoom

    def resize_window(self, size):
        self.window_size = size
        self.set_window()

    def update(self, game_obj):
        for event in game_obj.events:
            if event.type == pygame.VIDEORESIZE:
                new_size = Vector(event.w, event.h)
                self.resize_window(new_size)

    def set_zoom(self, zoom):
        self.zoom = zoom
        self.set_window()

    def draw_grid(self, xy_max=5, line_width=0.05, line_color=(200, 200, 200)):
        num_lines = (xy_max + 1) * 2
        lines = []
        for i in range(1, num_lines):
            lines.append(Line(Vector(i - num_lines // 2, -num_lines // 2), Vector(i - num_lines // 2, num_lines // 2)))
            lines.append(Line(Vector(-num_lines // 2, i - num_lines // 2), Vector(num_lines // 2, i - num_lines // 2)))
        for line in lines:
            self.draw_line(line, line_width, line_color)

    def draw_axes(self, line_width=0.1, radius=5, x_color=(0, 200, 0), y_color=(200, 0, 0)):
        x_line = Line(Vector(-radius, 0), Vector(radius, 0))
        y_line = Line(Vector(0, -radius), Vector(0, radius))
        self.draw_line(y_line, color=y_color, width=line_width)
        self.draw_line(x_line, color=x_color, width=line_width)

    def draw_rect(self, pos, size, color):
        pygame.draw.rect(self.window, color, self.display_rect(pos, size))

    def draw_circle(self, pos, radius=0.2, color=(0, 0, 0)):
        pygame.draw.circle(self.window, color, self.display_pos(pos).rounded().tuple(), int(radius * self.window_scale))

    def draw_line(self, line, width=0.1, color=(0, 0, 0)):
        pygame.draw.line(self.window, color, self.display_pos(line.pos1).tuple(), self.display_pos(line.pos2).tuple(), int(width * self.window_scale))

    def update_display(self):
        pygame.display.update()

    def clear_display(self, color=(255, 255, 255)):
        self.window.fill(color)

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
