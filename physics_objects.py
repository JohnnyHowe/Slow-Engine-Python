""" An object with physics properties like collision and gravity """
import pygame

from .vectors import Vector

GRAVITY_ACCELERATION = 9.8


class Object:
    def __init__(self, pos=Vector(0, 0), size=Vector(1, 1)):
        self.pos = pos
        self.size = size
        self.velocity = Vector(0, 0)
        self.gravity = False
        self.collider = None
        self.mass = self.size.x * self.size.y

    def update(self, game_obj):
        self.update_physics(game_obj)

    def update_physics(self, game_obj):
        if self.gravity:
            self.apply_gravity(game_obj)
        self.move_player(game_obj)

    def left(self):
        return self.pos.x - self.size.x / 2

    def right(self):
        return self.pos.x + self.size.x / 2

    def top(self):
        return self.pos.y - self.size.y / 2

    def bottom(self):
        return self.pos.y + self.size.y / 2

    def show(self, window_obj):
        self.show_block(window_obj)

    def move_player(self, game_obj):
        self.pos += self.velocity * game_obj.dtime

    def show_block(self, window_obj, color=(0, 0, 0)):
        window_obj.draw_rect(self.pos, self.size, color)

    def apply_gravity(self, game_obj):
        self.velocity.y -= GRAVITY_ACCELERATION * game_obj.dtime

    def __str__(self):
        rounding_dp = 2
        return "Object2d({}, {}, {}, {})".format(round(self.pos.x, rounding_dp),
                                                 round(self.pos.y, rounding_dp),
                                                 round(self.size.x, rounding_dp),
                                                 round(self.size.y, rounding_dp))


class BoxCollider:
    def __init__(self, parent_obj):
        self.parent_obj = parent_obj
        self.fixed = False
        # self.collide_with = "ALL"
        # self.collide_tag = "NONE"

    def collision_side(self, object2):
        """ object2 (BoxCollider2d)
        Return 2 valued tuple: Side that object2 has hit. """
        object1 = self.parent_obj
        relative_velocity = object1.velocity - object2.velocity
        overlap = Vector(min(object1.right(), object2.right()) - max(object1.left(), object2.left()),
                         min(object1.bottom(), object2.bottom()) - max(object1.top(), object2.top()))
        movement = Vector(relative_velocity.x / overlap.x, relative_velocity.y / overlap.y)
        if movement.x:
            movement.x /= abs(movement.x)
        if movement.y:
            movement.y /= abs(movement.y)
        return movement


