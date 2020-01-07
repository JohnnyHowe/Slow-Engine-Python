from math import sqrt
from .game_display import draw_game_rect, draw_game_circle
from .geometery import *

GRAVITATIONAL_CONSTANT = 9.8


class BoxObject:
    def __init__(self, rect):
        """
        Args:
            rect (Rect): Rect of box (in game units).
            mass (int): Mass of object (If None, mass will be set to width * height).
        """
        self.rect = rect
        self.velocity = Vector(0, 0)
        self.max_velocity = float("inf")

        self.controller = None
        self.collider = None
        self.gravity = False

    def show_block(self, engine, color=(0, 200, 0)):
        draw_game_rect(engine.window, self.rect, color)

    def show_circle(self, engine, color=(0, 200, 0)):
        draw_game_circle(engine.window, self.rect.pos(), min(self.rect.size()) / 2, color)

    def apply_velocity(self, engine):
        self.rect.set_pos(self.rect.pos() + self.velocity * engine.clock.dtime)

    def update(self, engine):
        self.cap_velocity()
        self.update_controller(engine)
        self.apply_velocity(engine)

    def update_controller(self, engine):
        if self.controller:
            self.controller.update(engine)

    def cap_velocity(self):
        current_velocity = self.velocity.length()
        scale = current_velocity / self.max_velocity
        if scale > 1:
            self.velocity.x /= scale
            self.velocity.y /= scale

    def apply_gravity(self, engine):
        self.velocity.y -= engine.clock.dtime * GRAVITATIONAL_CONSTANT

    def __str__(self):
        collider_str = None
        if self.collider:
            collider_str = self.collider.__str__()
        return "BoxObject({}, collider={})".format(tuple(round(self.rect)), collider_str)

    def __repr__(self):
        return self.__str__()


class BoxCollider:
    def __init__(self, parent, bounce=0, mass=None):
        """
        Args:
            parent (BoxObject): Object to have velocity, pos, etc viewed and changed.
            bounce (int): how bouncy is the object? 1 = perfect bounce, 0 = no bounce.
        """
        self.parent = parent
        self.bounce = bounce

        if mass is not None: self.mass = mass
        else: self.mass = parent.rect.w * parent.rect.h

    def has_collided_with(self, colliders):
        """ Has self collided with any of the colliders? """
        for collider in colliders:
            if self.is_collided_box(collider):
                return True
        return False

    def run_collisions(self, colliders=[], objects=[]):
        for collider in colliders:
            self.run_object_collision(collider)
        for obj in objects:
            self.run_object_collision(obj.collider)

    def run_object_collision(self, collider):
        if isinstance(collider, BoxCollider):
            self.box_collision(collider)
        else:
            raise Exception("Attempting to detect collision between box and non-box.")

    def box_overlap(self, other):
        """ What is the size of the overlap between self and other? """
        if self.is_collided_box(other):
            return Vector(abs(min(self.parent.rect.right(), other.parent.rect.right())
                              - max(self.parent.rect.left(), other.parent.rect.left())),
                          abs(min(self.parent.rect.top(), other.parent.rect.top())
                              - max(self.parent.rect.bottom(), other.parent.rect.bottom())))
        else:
            return Vector(0, 0)

    def box_collision_side(self, other):
        """ What side has self collided with other on? """
        overlap = self.box_overlap(other)
        if overlap.x or overlap.y:
            side = Vector(0, 0)
            if abs(overlap.x) > abs(overlap.y):
                side.y = 1
            else:
                side.x = 1
            if self.parent.rect.x > other.parent.rect.x:
                side.x = -side.x
            if self.parent.rect.y > other.parent.rect.y:
                side.y = -side.y
            return side
        else:
            return Vector(0, 0)

    def is_collided_box(self, other):
        """ Is there some overlap between self and other? """
        return (self.parent.rect.left() < other.parent.rect.right() and
                self.parent.rect.right() > other.parent.rect.left() and
                self.parent.rect.bottom() < other.parent.rect.top() and
                self.parent.rect.top() > other.parent.rect.bottom())

    def box_collision(self, other):
        """ If self has collided with other, move them so they aren't collided. """
        collision_side = self.box_collision_side(other)
        if (self.mass == other.mass == float("inf") or
            self.mass == other.mass == 0):
            raise Exception("TWO OBJECTS WITH INFINITE MASS COLLIDED WTF DO I DO.")
        else:
            if collision_side.x or collision_side.y:
                self.box_collision_rectify_pos(other, collision_side)
                self.box_collision_rectify_velocity(other, collision_side)

    def box_collision_rectify_velocity(self, other, collision_side):
        """ Assuming a collision on the y axis, rectify the velocity in the y axis.
        Assumes either self or other have real masses (not inf).

        Args:
            other (BoxCollider): collider that self has collided with.
            collision_side (Vector): Side of self that has collided with other.
        """
        if self.mass == float("inf") or other.mass == 0:
            other.box_collision_rectify_velocity(self, collision_side)
        elif other.mass == float("inf") or self.mass == 0:
            self.fixed_elastic_collision(other, collision_side)
        else:
            # UNFINISHED
            self.inelastic_collision(other, collision_side)

    def fixed_elastic_collision(self, other, collision_side):
        """ Run an elastic collision between self and other where other is fixed (mass=inf).
        So really just flip the velocity on the axis and scale it according to the bounce of
        self and other.

        Args:
            other (BoxCollider): collider that self has collided with.
        """
        bounce = max(self.bounce, other.bounce)
        if collision_side.x:
            relative_velocity = other.parent.velocity.x - self.parent.velocity.x
            self.parent.velocity.x *= -1
            self.parent.velocity.x -= relative_velocity * (1 - bounce)
        else:
            relative_velocity = other.parent.velocity.y - self.parent.velocity.y
            self.parent.velocity.y *= -1
            self.parent.velocity.y -= relative_velocity * (1 - bounce)

    def inelastic_collision(self, other, collision_side):
        """ Run an inelastic collision between self and other where both have real masses. """
        if collision_side.x:
            self_velocity = self.parent.velocity.x
            other_velocity = other.parent.velocity.x
        else:
            self_velocity = self.parent.velocity.y
            other_velocity = other.parent.velocity.y

        self_momentum = self.mass * self_velocity
        other_momentum = other.mass * other_velocity

        total_momentum = self_momentum + other_momentum
        total_mass = self.mass + other.mass
        final_velocity = total_momentum / total_mass

        if collision_side.x:
            self.parent.velocity.x = final_velocity
            other.parent.velocity.x = final_velocity
        else:
            self.parent.velocity.y = final_velocity
            other.parent.velocity.y = final_velocity

    def box_collision_rectify_pos(self, other, collision_side):
        """ Assuming a collision, rectify the pos. """
        self_rect = self.parent.rect
        other_rect = other.parent.rect
        if collision_side.x:
            self_rect.x = other_rect.x - collision_side.x * (other_rect.w + self_rect.w) / 2
        else:
            self_rect.y = other_rect.y - collision_side.y * (other_rect.h + self_rect.h) / 2

    def __str__(self):
        return "BoxCollider"

