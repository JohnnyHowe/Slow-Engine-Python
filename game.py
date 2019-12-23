import pygame

from .window import Window
from .vectors import Vector
from .sprites import SpriteSheet


class Game:
    def __init__(self):
        pygame.init()
        self.window = Window(self, Vector(800, 600))

        self.dtime = 0
        self.time_since_start = 0
        self.clock = pygame.time.Clock()
        self.events = []
        self.keys_pressed = []

        self.objects = []

    def update(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.dtime = min(self.clock.tick() / 1000, 0.01)
        self.time_since_start += self.dtime
        for item in self.objects:
            item.update(self)
        self.event_loop()
        self.window.update(self)

    def draw_objects(self):
        # self.window_obj.window.fill((255, 255, 255))
        for item in self.objects:
            item.show(self.window)

    def event_loop(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                quit()

    def mouse_pos(self):
        real_pos = pygame.mouse.get_pos()
        return self.window.real_pos(Vector(real_pos[0], real_pos[1]))


