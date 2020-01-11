from math import sqrt
from slowEngine.game_display import draw_game_rect, draw_game_circle
from slowEngine.geometery import *

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

    def get_collision_rect(self):
        return self.rect

    def get_display_rect(self):
        return self.rect

    def show_block(self, engine, color=(0, 200, 0), width=None):
        use_rect = self.get_display_rect()
        draw_game_rect(engine.window, use_rect, color, width=width)

    def show_circle(self, engine, color=(0, 200, 0)):
        draw_game_circle(engine.window, self.get_display_rect().pos(), min(self.get_display_rect().size()) / 2, color)

    def apply_velocity(self, engine):
        self.rect.set_pos(self.rect.pos() + self.velocity * engine.clock.dtime)
        self.cap_velocity()

    def update(self, engine):
        self.cap_velocity()
        self.update_controller(engine)
        self.apply_velocity(engine)

    def update_controller(self, engine):
        if self.controller:
            self.controller.update(engine)

    def cap_velocity(self):
        if isinstance(self.max_velocity, Vector):
            self.velocity.x = min(max(self.velocity.x, -self.max_velocity.x), self.max_velocity.x)
            self.velocity.y = min(max(self.velocity.y, -self.max_velocity.y), self.max_velocity.y)
        else:
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

        if mass is not None:
            self.mass = mass
        else:
            self.mass = parent.get_collision_rect().w * parent.rect.h

    def has_collided_with(self, colliders):
        """ Has self collided with any of the colliders? """
        for collider in colliders:
            collision = self.is_collided_box(collider)
            if collision:
                return collision
        return False

    def run_collisions(self, colliders=[], objects=[]):
        collisions = []
        for collider in colliders:
            collision = self.run_object_collision(collider)
            if collision:
                collisions.append(collision)
        for obj in objects:
            collision = self.run_object_collision(obj.collider)
            if collision:
                collisions.append(collision)
        return collisions

    def run_object_collision(self, collider):
        """ Check if self and collider have collided.

        Args:
            collider (Collider): object/collider to check for collision.

        Returns:
            collision (Collision or None):  if None: objects didn't collide.

        """
        if isinstance(collider, BoxCollider):
            return self.box_collision(collider)
        else:
            raise Exception("Attempting to detect collision between box and non-box.")

    def box_overlap(self, other, negatives=False):
        """ What is the size of the overlap between self and other? """
        if self.is_collided_box(other) or negatives:
            overlap = Vector(min(self.parent.get_collision_rect().right(),
                                 other.parent.get_collision_rect().right())
                             - max(self.parent.get_collision_rect().left(),
                                   other.parent.get_collision_rect().left()),
                             min(self.parent.get_collision_rect().top(),
                                 other.parent.get_collision_rect().top())
                             - max(self.parent.get_collision_rect().bottom(),
                                   other.parent.get_collision_rect().bottom()))
        else:
            overlap = Vector(0, 0)
        if not negatives:
            overlap = abs(overlap)
        return overlap

    def box_collision_side(self, other):
        """ What side has self collided with other on? """
        overlap = self.box_overlap(other)
        if overlap.x or overlap.y:
            side = Vector(0, 0)
            if abs(overlap.x) > abs(overlap.y):
                side.y = 1
            else:
                side.x = 1
            if self.parent.get_collision_rect().x > other.parent.get_display_rect().x:
                side.x = -side.x
            if self.parent.get_collision_rect().y > other.parent.get_collision_rect().y:
                side.y = -side.y
            return side
        else:
            return Vector(0, 0)

    def is_touching_box(self, other):
        """ Is self touching other?
        This differs to is_collided_box by the boundaries.
        is_collided_box only checks for greater or less than. this checks equality as well. """
        return (self.parent.get_collision_rect().left() <= other.parent.get_collision_rect.right() and
                self.parent.get_collision_rect().right() >= other.parent.get_collision_rect.left() and
                self.parent.get_collision_rect().bottom() <= other.parent.get_collision_rect.top() and
                self.parent.get_collision_rect().top() >= other.parent.get_collision_rect.bottom())

    def box_touching_side(self, other):
        """ What side of self is touching other? """
        overlap = self.box_overlap(other, negatives=True)
        side = Vector(0, 0)
        if overlap.x == overlap.y == 0:
            return Vector(0, 0)
        if abs(overlap.x) > abs(overlap.y):
            side.y = -1
            if other.parent.get_collision_rect().y > self.parent.get_collision_rect().y:
                side.y = 1
        if abs(overlap.x) < abs(overlap.y):
            side.x = -1
            if other.parent.get_collision_rect().x > self.parent.get_collision_rect().x:
                side.x = 1
        return side

    def is_collided_box(self, other):
        """ Is there some overlap between self and other? """
        return (self.parent.get_collision_rect().left() < other.parent.get_collision_rect().right() and
                self.parent.get_collision_rect().right() > other.parent.get_collision_rect().left() and
                self.parent.get_collision_rect().bottom() < other.parent.get_collision_rect().top() and
                self.parent.get_collision_rect().top() > other.parent.get_collision_rect().bottom())

    def box_collision(self, other):
        """ If self has collided with other, move them so they aren't collided.

        Args:
            other (BoxCollider): collider/object to check collision for.

        Returns:
            collision (Collision or None):  if None: objects didn't collide.
        """
        collision_side = self.box_collision_side(other)
        collision = None
        if (self.mass == other.mass == float("inf") or
                self.mass == other.mass == 0):
            raise Exception("TWO OBJECTS WITH INFINITE MASS COLLIDED WTF DO I DO.")
        else:
            if collision_side.x or collision_side.y:
                collision = BoxCollision(self, other, collision_side)
                self.box_collision_rectify_pos(other, collision_side)
                self.box_collision_rectify_velocity(other, collision_side)
        return collision

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
        self_rect = self.parent.get_collision_rect()
        other_rect = other.parent.get_collision_rect()
        if collision_side.x:
            self_rect.x = other_rect.x - collision_side.x * (other_rect.w + self_rect.w) / 2
        else:
            self_rect.y = other_rect.y - collision_side.y * (other_rect.h + self_rect.h) / 2

    def __str__(self):
        return "BoxCollider"


class BoxCollision:
    """ An object that holds all the information about a collision. """

    def __init__(self, object1, object2, collision_side):
        self.object1 = object1
        self.object2 = object2
        if collision_side is None:
            self.collision_side = Vector(0, 0)
        else:
            self.collision_side = collision_side
