import slowEngine
from slowEngine.geometery import Vector


def main():
    engine = slowEngine.Engine()
    engine.set_window(Vector(400, 400))

    width = 0.05
    wall_rects = [
        (1, -5, 8, width),
        (0, 5, 10, width),
        (5, 0, width, 10),
        (-5, 0, width, 10),
    ]

    walls = []
    for rect in wall_rects:
        wall = slowEngine.physics.BoxObject(Vector(rect[0], rect[1]), Vector(rect[2], rect[3]))
        wall.collider = slowEngine.physics.BoxCollider(wall)
        wall.mass = float("inf")
        walls.append(wall)

    player = slowEngine.physics.BoxObject(Vector(0, 0), Vector(1, 1))
    player.collider = slowEngine.physics.BoxCollider(player)
    player.controller = slowEngine.controllers.KeyBoardControllerSmooth(player, slowEngine.controllers.WASD_Controls)

    while True:
        engine.update()

        player.update(engine)
        player.controller.update(engine)

        engine.window.fill()

        for wall in walls:
            wall.update(engine)
            player.collider.box_collision(wall.collider)
            wall.show_block(engine, (0, 0, 0))

        player.show_block(engine)
        engine.window.update_display()


if __name__ == "__main__":
    main()
