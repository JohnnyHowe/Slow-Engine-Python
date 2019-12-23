import slowEngine
import pygame


def main():

    game = slowEngine.Game()

    block = slowEngine.PhysicsObject(pos=slowEngine.Vector(0, -2.5), size=slowEngine.Vector(8, 1))
    block.collider = slowEngine.BoxCollider(block)

    mouse_line = slowEngine.Line(slowEngine.Vector(0, 0), slowEngine.Vector(0, 0))

    game.objects.append(block)

    while True:

        game.update()
        mouse_line.pos2 = game.mouse_pos()
        intersections = mouse_line.box_intersections(block.collider)

        game.window.clear_display()
        game.window.draw_grid()
        game.draw_objects()

        if game.keys_pressed[pygame.K_ESCAPE]:
            quit()

        for pos, side in intersections:
            game.window.draw_circle(pos, color=(255, 0, 255))

        game.window.draw_line(mouse_line, color=(0, 0, 255))
        game.window.update_display()


if __name__ == "__main__":
    main()
