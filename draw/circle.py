import pygame
from slowEngine.display import Display
from slowEngine.camera import Camera


def draw_world_circle(color, position, radius, width=None):
    new_position = Camera.world_to_display_position(position)
    size = Camera.get_display_size()

    if width is None:
        draw_screen_circle(color, new_position, radius * size)
    else:
        draw_screen_circle(color, new_position, radius * size, width * size)


def draw_screen_circle(color, position, radius, width=None):
    if width is None:
        pygame.draw.circle(Display.surface, color, position.get_pygame_tuple(), int(radius))
    else:
        pygame.draw.circle(Display.surface, color, position.get_pygame_tuple(), int(radius), int(width))
