import slowEngine
from slowEngine.vectors import Vector


class TestSprite:
    def __init__(self):
        self.pos = Vector(0, 0)

        self.sprite = slowEngine.sprites.CompositeSprite({
            "FACES": slowEngine.sprites.Sprite("images/faces.png", Vector(1, 1)),
            "POSES": slowEngine.sprites.Sprite("images/poses.png", Vector(1, 1)),
        }, [("POSES->MIDDLE", "FACES->MIDDLE")]
        )

    def update(self, game_obj):
        self.sprite.sprites["FACES"].cycle_images(game_obj, "DEFAULT", 1)
        self.sprite.sprites["POSES"].cycle_images(game_obj, "DEFAULT", 1)

    def show(self, window_obj):
        self.sprite.show(window_obj, self.pos, "POSES->MIDDLE")


def main():
    game = slowEngine.Game()
    test_sprite = TestSprite()

    while True:
        game.update()
        test_sprite.update(game)
        game.window_obj.window.fill((255, 255, 255))
        test_sprite.show(game.window_obj)
        game.show()


main()
