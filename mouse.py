import pygame
from .geometery import Vector
from .game_display import game_pos


class Mouse:
    def __init__(self):
        self.pos = Vector(0, 0)
        self.window_pos = Vector(0, 0)
        self.pos_change = Vector(0, 0)
        self.buttons = [0, 0, 0]
        self.button_states = [0, 0, 0]

    def update(self, engine):
        self.update_pos(engine)
        self.update_buttons()

    def update_pos(self, engine):
        old_pos = self.pos
        mouse_pos = pygame.mouse.get_pos()
        self.window_pos = Vector(mouse_pos[0], mouse_pos[1])
        self.pos = game_pos(self.window_pos, engine.window)
        self.pos_change = self.pos - old_pos

    def update_buttons(self):
        old_buttons = self.buttons
        self.buttons = pygame.mouse.get_pressed()
        self.button_states = [self.buttons[i] - old_buttons[i] for i in range(3)]

