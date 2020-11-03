import pygame
from slowEngine.vector2 import Vector2


class _Display:

    surface = None
    size = None

    """ Object to control the pygame window. """
    def __init__(self):
        pygame.init()
        self.set_window(Vector2(600, 400))
        self.set_caption("SlowEngine")

    @staticmethod
    def set_caption(caption):
        pygame.display.set_caption(str(caption))

    def set_window(self, size):
        """ Set self.size (Vector), self.window (pygame.Surface) and self.game_scale. """
        self.size = size
        self.surface = pygame.display.set_mode(tuple(size), pygame.RESIZABLE)

    def fill(self, color=(255, 255, 255)):
        """ Fill the window with a solid color. """
        self.surface.fill(color)

    @staticmethod
    def update_display():
        """ Update the surface so the drawn items are displayed. """
        pygame.display.update()


Display = _Display()
