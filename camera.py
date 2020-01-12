from slowEngine.geometery import *
import pygame


class Camera:
    """ Camera object. """
    def __init__(self):
        self.pos = Vector(0, 0)


def apply_offset_pos(camera, pos):
    return pos - camera.pos


def apply_offset_rect(camera, rect):
    return rect - Rect(camera.x, camera.y, camera.x, camera.y)


