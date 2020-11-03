import pygame

from slowEngine.display import Display
from slowEngine.camera import Camera


def draw_world_text(text, color, position, font_size=1, font_name="arial"):
    """ Draw some text in the world (world coordinates).

    Args:
        text: string to show
        color: color to show text as
        position: where to center text on
        font_size: font size of text
        font_name: name of font to use
    """
    new_position = Camera.world_to_display_position(position)
    draw_screen_text(text, color, new_position, int(font_size * Camera.get_display_size()), font_name)


def draw_screen_text(text, color, position, font_size=20, font_name="arial"):
    """ Draw some text on the screen (screen coordinates).

    Args:
        text: string to show
        color: color to show text as
        position: where to center text on
        font_size: font size of text
        font_name: name of font to use
    """
    font = pygame.font.SysFont(font_name, font_size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    display_position = (position.x - text_rect.w / 2, position.y - text_rect.h / 2)
    Display.surface.blit(text_surface, display_position)
