from math import sqrt
from .game_display import draw_game_rect, draw_game_circle
from .geometery import *


class BoxObject:
    def __init__(self, rect, mass=None):
        """
        Args:
            rect (Rect): Rect of box (in game units).
            mass (int): Mass of object (If None, mass will be set to width * height).
        """
        self.rect = rect

        if mass is not None: self.mass = mass
        else: self.mass = rect.w * rect.h

        self.velocity = Vector(0, 0)
        self.max_velocity = float("inf")

        self.controller = None
        self.collider = None

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

    def __str__(self):
        collider_str = None
        if self.collider:
            collider_str = self.collider.__str__()
        return "BoxObject({}, collider={})".format(tuple(round(self.rect)), collider_str)

    def __repr__(self):
        return self.__str__()


class BoxCollider:
    def __init__(self, parent, bounce=0):
        """
        Args:
            parent (BoxObject): Object to have velocity, pos, etc viewed and changed.
            bounce (int): how bouncy is the object? 1 = perfect bounce, 0 = no bounce.
        """
        self.parent = parent
        self.bounce = bounce

    def is_collided_with(self, colliders):
        """ Has self collided with any of the colliders? """
        for collider in colliders:
            if self.is_collided_box(collider):
                return True
        return False

    def run_collisions(self, colliders):
        """ Loop through all the colliders and run the collision code. """
        for collider in colliders:
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
        if (self.parent.mass == other.parent.mass == float("inf") or
            self.parent.mass == other.parent.mass == 0):
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
        if self.parent.mass == float("inf") or other.parent.mass == 0:
            other.box_collision_rectify_velocity(self, collision_side)
        elif other.parent.mass == float("inf") or self.parent.mass == 0:
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

        self_momentum = self.parent.mass * self_velocity
        other_momentum = other.parent.mass * other_velocity

        total_momentum = self_momentum + other_momentum
        total_mass = self.parent.mass + other.parent.mass
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

