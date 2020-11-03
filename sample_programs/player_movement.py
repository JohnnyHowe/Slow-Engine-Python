""" Sample program for the SlowEngine.
Shows off basic 2D player movement. No bells or whistles. """
import slowEngine
import pygame


class Game:

    player = None

    def __init__(self):
        self.player = Player()

    def run(self):
        while True:
            self.run_frame()

    def run_frame(self):
        slowEngine.EventHandler.run()
        slowEngine.Display.fill((255, 255, 255))

        self.player.show()

        slowEngine.Display.update_display()


class Player:

    position = None

    def __init__(self):
        self.position = slowEngine.Vector2(0, 0)

    def show(self):
        slowEngine.draw.draw_world_circle((0, 255, 0), self.position, 0.5)
        slowEngine.draw.draw_world_circle((0, 0, 0), self.position, 0.5, 0.05)
        slowEngine.draw.draw_world_text("Hoes", (0, 0, 0), self.position + slowEngine.Vector2(0, 1), 0.5)


if __name__ == "__main__":
    Game().run()
