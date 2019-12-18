import pygame

from .window import Window
from .vectors import Vector
from .physics_handler import PhysicsHandler
from .sprites import SpriteSheet


class Game:
    def __init__(self):
        pygame.init()
        self.window_obj = Window(Vector(800, 600))

        self.dtime = 0
        self.time_since_start = 0
        self.clock = pygame.time.Clock()
        self.pygame_events = []
        self.keys_pressed = []

        self.objects = []
        self.physics_handler = PhysicsHandler(self.objects)

    def update(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.dtime = min(self.clock.tick() / 1000, 0.01)
        self.time_since_start += self.dtime
        for item in self.objects:
            item.update(self)
        self.event_loop()

    def show(self):
        # self.window_obj.window.fill((255, 255, 255))
        for item in self.objects:
            item.show(self.window_obj)
        pygame.display.update()

    def event_loop(self):
        self.pygame_events = pygame.event.get()
        for event in self.pygame_events:
            if event.type == pygame.QUIT:
                quit()


