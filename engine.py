import pygame
from .window import Window
from .camera import Camera


class Engine:
    def __init__(self):
        self.window = None
        self.camera = Camera()
        self.events = {}

    def update(self):
        self.window.update(self)
        self.set_event_dict()

    def set_window(self, size, units_per_axis=10):
        self.window = Window(size, units_per_axis)

    def set_event_dict(self):
        self.events = {}
        for event in pygame.event.get():
            self.events[event.type] = event
