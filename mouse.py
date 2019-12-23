import pygame
from .vectors import Vector


class Mouse:
    def __init__(self):
        self.pos = Vector(0, 0)
        self.window_pos = Vector(0, 0)
        self.buttons = [0, 0, 0]
        self.button_states = [0, 0, 0]

    def update(self, game_obj):
        mouse_pos = pygame.mouse.get_pos()
        self.window_pos = Vector(mouse_pos[0], mouse_pos[1])
        self.pos = game_obj.window.real_pos(self.window_pos)

        old_buttons = self.buttons
        self.buttons = pygame.mouse.get_pressed()
        self.button_states = [self.buttons[i] - old_buttons[i] for i in range(3)]
