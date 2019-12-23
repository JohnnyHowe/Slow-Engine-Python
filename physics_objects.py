""" An object with physics properties like collision and gravity """
import pygame
import math

from .vectors import Vector
from .coordinate_geometry import Line


GRAVITY_ACCELERATION = 9.8 * 3.5


class PhysicsObject:
    def __init__(self, pos=Vector(0, 0), size=Vector(1, 1), **kwargs):
        self.pos = pos
        self.size = size
        self.velocity = Vector(0, 0)
        self.gravity = False
        self.collider = None
        self.friction = 0
        self.mass = self.size.x * self.size.y
        self.set_kwargs(kwargs)
        self.max_speed = Vector(float("inf"), float("inf"))

    def set_kwargs(self, kwargs):
        for keyword, value in kwargs.items():
            exec("self.{} = {}".format(keyword, value))

    def update(self, game_obj):
        self.physics_update(game_obj)

    def physics_update(self, game_obj):
        self.move_player(game_obj)
        if self.gravity:
            self.apply_gravity(game_obj)
        if self.collider:
            self.collider_update(game_obj)

    def collider_update(self, game_obj):
        self.apply_friction(game_obj)
        self.collider.update(game_obj)

    def left(self):
        """ Return x-ordinate of the left side of the object (x pos - width / 2). """
        return self.pos.x - self.size.x / 2

    def right(self):
        """ Return x-ordinate of the right side of the object (x pos + width / 2). """
        return self.pos.x + self.size.x / 2

    def top(self):
        """ Return y-ordinate of the top of the object (y pos + height / 2). """
        return self.pos.y - self.size.y / 2

    def bottom(self):
        """ Return y-ordinate of the bottom of the object (y pos - height / 2). """
        return self.pos.y + self.size.y / 2

    def top_left(self):
        """ Return the position Vector of the top left corner. """
        return self.pos + Vector(-self.width, self.height) / 2

    def top_right(self):
        """ Return the position Vector of the top right corner. """
        return self.pos + Vector(self.width, self.height) / 2

    def bottom_left(self):
        """ Return the position Vector of the bottom left corner. """
        return self.pos + Vector(-self.width, -self.height) / 2

    def bottom_right(self):
        """ Return the position Vector of the bottom_right corner. """
        return self.pos + Vector(self.width, -self.height) / 2

    def show(self, window_obj):
        self.show_block(window_obj)

    def move_player(self, game_obj):
        """ Apply self.velocity to self.pos. """
        self.velocity.x = max(min(self.velocity.x, self.max_speed.x), -self.max_speed.x)
        self.pos += self.velocity * game_obj.dtime

    def show_block(self, window_obj, color=(0, 0, 0)):
        """ Draw object as a solid block of color.

        Args:
            window_obj (Window): window object to draw block on.
            color (Tuple): colour of block to draw in (r, g, b).

        Returns:
            None
        """
        window_obj.draw_rect(self.pos, self.size, color)

    def apply_gravity(self, game_obj):
        """ Decrease self.velocity, emulating gravity. """
        self.velocity.y -= GRAVITY_ACCELERATION * game_obj.dtime

    def apply_friction(self, game_obj):
        for other in self.collider.contact[(0, 1)] + self.collider.contact[(0, -1)]:
            if other.fixed:

                friction = self.friction * other.parent_obj.friction
                normal_force = self.mass * GRAVITY_ACCELERATION

                friction_force = friction * normal_force
                friction_deceleration = friction_force / self.mass

                if self.velocity.x:
                    velocity_change = friction_deceleration * game_obj.dtime * (self.velocity.x / abs(self.velocity.x))
                    if abs(velocity_change) > abs(self.velocity.x):
                        self.velocity.x = 0
                    else:
                        self.velocity.x -= velocity_change

    def wasd_movement(self, game_obj):
        """ If self.keyboard_movement, move the object from WASD key input. """
        speed = game_obj.dtime * 5
        movement_keys = {
            (1, 0): pygame.K_d,
            (-1, 0): pygame.K_a,
            (0, 1): pygame.K_w,
            (0, -1): pygame.K_s,
        }
        pressed_keys = pygame.key.get_pressed()
        for movement, key in movement_keys.items():
            if pressed_keys[key]:
                self.pos += Vector(movement[0], movement[1]) * speed

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
        self.contact = {}
        self.reset_contact()

    def reset_contact(self):
        self.contact = {
            (1, 0): [],
            (-1, 0): [],
            (0, 1): [],
            (0, -1): [],
        }

    def update(self, game_obj):
        self.handle_collisions(game_obj)
        self.reset_contact()
        for other in game_obj.objects:
            if other != self.parent_obj:
                self.update_contact(other.collider)

    def update_contact(self, other):
        if self.touching(other):
            self.contact[self.box_collision_side(other).tuple()].append(other)

    def handle_collisions(self, game_obj):
        """ If there has been a collision, stop the object's movement (in correct plane) and fix
        object's position. """
        for side, objects in self.contact.items():
            for obj in objects:
                self.fix_position(obj, Vector(side[0], side[1]))

    def fix_position(self, other, collision_side):
        """ Move self so that there is no overlap between self and other.
        Call the same method on other as well.

        Args:
            other (collider): other collider to move.

        Returns:
            None
        """
        if self.fixed:
            return
        elif other.fixed:
            overlap = self.overlap(other)

            self.parent_obj.pos.x -= collision_side.x * overlap.x
            self.parent_obj.pos.y -= collision_side.y * overlap.y

            if self.parent_obj.velocity.y * collision_side.y > 0:
                self.parent_obj.velocity.y = 0
            if self.parent_obj.velocity.x * collision_side.x > 0:
                self.parent_obj.velocity.x = 0
        else:
            raise ValueError("BoxCollider.fix_position given a collider not ready to handle.")

    def box_collision_side(self, other):
        """ Find the side of self that has collided with other.

        Value returned is a vector. (0, 0) for no collision.
        (1, 0) for right, (-1, 0) for left, (0, 1) for top, (0, -1) for bottom.
        (0, 0) for no collision

        Args:
            other (BoxCollider): object that (may have) collided with self.

        Returns:
            side (Vector): Side of self that other has collided with.
        """
        overlap = self.overlap(other)
        side = Vector(0, 0)
        if abs(overlap.x) > abs(overlap.y):
            side.y = 1
        else:
            side.x = 1
        if self.parent_obj.pos.x > other.parent_obj.pos.x:
            side.x = -side.x
        if self.parent_obj.pos.y > other.parent_obj.pos.y:
            side.y = -side.y
        return side

    def closest_corner(self, pos):
        """ What corner of self is closest to pos?

        Args:
            pos (Vector): position to find closest corner to

        Returns:
            corner (Vector): Corner of self that is closest to other. """
        corner = Vector(1, 1)
        if abs(self.parent_obj.left() - pos.x) < abs(self.parent_obj.right() - pos.x):
            corner.x = -1
        if abs(self.parent_obj.top() - pos.y) < abs(self.parent_obj.bottom() - pos.y):
            corner.y = -1
        return corner

    def overlap(self, other):
        """ Find the size of the overlap between self and other.

        Args:
            other (collider): Object that (might) overlap self.

        Returns:
            overlap (Vector): The size of the overlap of self and other.
        """
        if self.touching(other):
            if isinstance(other, BoxCollider):
                return self.box_overlap(other)
            else:
                raise ValueError("TRYING TO FIND OVERLAP OF BOX AND NON BOX THIS IS NOT CODED YET")
        return Vector(0, 0)

    def box_overlap(self, other):
        """ Find the size of the overlap between self and other, assuming both are BoxColliders.

        Args:
            other (BoxCollider): Object that (might) overlap with self.

        Returns:
            overlap (Vector): Size of the overlap of self and other.
            """
        return Vector(min(self.parent_obj.right(), other.parent_obj.right()) - max(self.parent_obj.left(), other.parent_obj.left()),
                      min(self.parent_obj.bottom(), other.parent_obj.bottom()) - max(self.parent_obj.top(), other.parent_obj.top()))

    def collided_with(self, other):
        """ Has other collider with self? (and vice-versa)

        Two objects are considered in a collision if they are touching and are moving closer together.

        Args:
            other (collider): Object that may have collided with self.

        Returns:
            collision (Bool): whether self and other have collided.
        """
        if isinstance(other, BoxCollider):
            return self.box_collision(other)
        else:
            raise ValueError("A NON BOX HAS COLLIDED WITH A BOX - THERE IS NO CODE TO HANDLE THIS")

    def box_collision(self, other):
        """ Has other collider with self? (and vice-versa)

        Two objects are considered in a collision if they are touching and are moving closer together.

        Args:
            other (BoxCollider): Object that may have collided with self.

        Returns:
            collision (Bool): whether self and other have collided.
        """
        relative_velocity = self.parent_obj.velocity - other.parent_obj.velocity
        return self.touching(other) and relative_velocity.length() > 0

    def touching(self, other):
        """ Is self touching other?

        Two objects are considered touching if and only if there is some overlap or there
        boundaries touch.

        Args:
            other (collider): object that may be touching self.

        Returns:
            touching (Bool): Whether self and other are touching.
        """
        if isinstance(other, BoxCollider):
            return self.box_touching(other)
        else:
            raise ValueError("CONTACT BETWEEN {} AND BoxCollider NOT CODED - BoxCollider.touching".format(type(other)))

    def box_touching(self, other):
        """ Is self touching other?

        Two objects are considered touching if and only if there is some overlap or there
        boundaries touch. Excluding corners.

        Args:
            other (collider): object that may be touching self.

        Returns:
            touching (Bool): Whether self and other are touching.
        """
        touching = (self.parent_obj.right() >= other.parent_obj.left() and
                    self.parent_obj.left() <= other.parent_obj.right() and
                    self.parent_obj.top() <= other.parent_obj.bottom() and
                    self.parent_obj.bottom() >= other.parent_obj.top())
        overlapping_x = (self.parent_obj.right() > other.parent_obj.left() and
                         self.parent_obj.left() < other.parent_obj.right())
        overlapping_y = (self.parent_obj.top() < other.parent_obj.bottom() and
                         self.parent_obj.bottom() > other.parent_obj.top())
        return touching and (overlapping_x or overlapping_y)

    def border_lines(self):
        """ Where are the borders of self?

        Args:
            None

        Returns:
            lines (List): A list of tuples containing the line and vector.
        """
        pos = self.parent_obj.pos
        size = self.parent_obj.size
        corners = {
            (-1, 1): Vector(pos.x - size.x / 2, pos.y + size.y / 2),
            (1, 1): Vector(pos.x + size.x / 2, pos.y + size.y / 2),
            (1, -1): Vector(pos.x + size.x / 2, pos.y - size.y / 2),
            (-1, -1): Vector(pos.x - size.x / 2, pos.y - size.y / 2),
        }
        return [
            (Line(corners[(-1, 1)], corners[(1, 1)]), Vector(0, 1)),
            (Line(corners[(1, 1)], corners[(1, -1)]), Vector(1, 0)),
            (Line(corners[(1, -1)], corners[(-1, -1)]), Vector(0, -1)),
            (Line(corners[(-1, -1)], corners[(-1, 1)]), Vector(-1, 0)),
        ]

