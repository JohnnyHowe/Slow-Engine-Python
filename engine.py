import pygame
from .mouse import Mouse
from .keys import KeyInput
from .window import Window
from .clock import Clock


class Engine:
    def __init__(self):
        self.window = None
        self.events = {}
        self.mouse = Mouse()
        self.keyboard = KeyInput()
        self.clock = Clock()

    def update(self):
        self.clock.update()
        self.set_event_dict()
        self.window.update(self)
        self.mouse.update(self)
        self.keyboard.update()

    def set_window(self, size):
        self.window = Window(size)

    def set_event_dict(self):
        self.events = {}
        for event in pygame.event.get():
            self.events[event.type] = event
