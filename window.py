import pygame
from .game_display import draw_game_line
from .geometery import *


class Window:
    """ Object to control the pygame window. """
    def __init__(self, size, units_per_axis=10):
        self.size = None
        self.units_per_axis = units_per_axis
        self.game_scale = None
        self.window = None
        self.set_window(size)

    def set_caption(self, caption):
        pygame.display.set_caption(str(caption))

    def set_window(self, size):
        """ Set self.size (Vector), self.window (pygame.Surface) and self.game_scale. """
        self.size = size
        self.game_scale = min(self.size) / self.units_per_axis
        self.window = pygame.display.set_mode(tuple(size), pygame.RESIZABLE)

    def fill(self, color=(255, 255, 255)):
        """ Fill the window with a solid color. """
        self.window.fill(color)

    @staticmethod
    def update_display():
        """ Update the surface so the drawn items are displayed. """
        pygame.display.update()

    def update(self, engine):
        self.quit_button(engine)
        self.control_size(engine)

    def quit_button(self, engine):
        """ If the window quit button is pressed, close down the game. """
        if pygame.QUIT in engine.events:
            quit()

    def control_size(self, engine):
        """ If the window has been resized, reset self.window etc. """
        if pygame.VIDEORESIZE in engine.events:
            event = engine.events[pygame.VIDEORESIZE]
            self.set_window(Vector(event.w, event.h))

    def draw_grid(self, xy_max=5, line_width=0.05, line_color=(200, 200, 200)):
        num_lines = (xy_max + 1) * 2
        lines = []
        for i in range(1, num_lines):
            lines.append(Line(Vector(i - num_lines // 2, -num_lines // 2), Vector(i - num_lines // 2, num_lines // 2)))
            lines.append(Line(Vector(-num_lines // 2, i - num_lines // 2), Vector(num_lines // 2, i - num_lines // 2)))
        for line in lines:
            draw_game_line(self, line, 1, line_color)

