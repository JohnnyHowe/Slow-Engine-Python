import pygame
from .geometery import *


class Window:
    """ Object to control the pygame window. """
    def __init__(self, size):
        self.size = None
        self.game_scale = None
        self.window = None
        self.set_window(size)

    def set_window(self, size):
        """ Set self.size (Vector), self.window (pygame.Surface) and self.game_scale. """
        self.size = size
        self.game_scale = min(size) / 20
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

