""" An object with physics properties like collision and gravity """
import pygame
import math

from .vectors import Vector


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
        self.apply_friction(game_obj)
        self.move_player(game_obj)
        if self.gravity:
            self.apply_gravity(game_obj)
        if self.collider:
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
            # collision_side = self.collider.box_collision_side(other.collider)
            if other.fixed:

                # friction = self.friction + (other.friction * (1 - self.friction))
                friction = self.friction * other.parent_obj.friction
                normal_force = self.mass * GRAVITY_ACCELERATION

                friction_force = friction * normal_force
                friction_deceleration = friction_force / self.mass

                if self.velocity.x:
                    self.velocity.x -= friction_deceleration * game_obj.dtime * (self.velocity.x / abs(self.velocity.x))

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
        # self.collide_with = "ALL"
        # self.collide_tag = "NONE"
        self.contact = {}
        self.reset_contact()

    def reset_contact(self):
        self.contact = {
            (1, 0): [],
            (-1, 0): [],
            (0, 1): [],
            (0, -1): [],
        }

    def update_contact(self, game_obj):
        self.reset_contact()
        for other in game_obj.objects:
            if other != self.parent_obj:
                if self.touching(other.collider):
                    self.contact[self.box_collision_side(other.collider).tuple()].append(other.collider)

    def update(self, game_obj):
        self.update_contact(game_obj)

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
        mock_self_obj = PhysicsObject(self.parent_obj.pos.copy(), self.parent_obj.size.copy())
        mock_self_obj.collider = BoxCollider(mock_self_obj)
        mock_other_obj = PhysicsObject(other.parent_obj.pos.copy(), other.parent_obj.size.copy())

        # Scale so other is a square
        y_scale = mock_other_obj.size.x / mock_other_obj.size.y
        mock_other_obj.size.y = mock_other_obj.size.x
        mock_other_obj.pos.y *= y_scale
        mock_self_obj.size.y *= y_scale
        mock_self_obj.pos.y *= y_scale

        closest_corner = mock_self_obj.collider.closest_corner(mock_other_obj.pos)
        closest_corner_pos = mock_self_obj.pos.copy()
        closest_corner_pos.x += (mock_self_obj.size.x / 2) * closest_corner.x
        closest_corner_pos.y += (mock_self_obj.size.y / 2) * closest_corner.y

        # Find angle between mock_other_obj and closest_corner
        angle = math.degrees(math.atan2(mock_other_obj.pos.y - closest_corner_pos.y,
                                        mock_other_obj.pos.x - closest_corner_pos.x))
        angle = (angle + 45) % 360
        side_number = int(angle / 90)
        side = Vector(0, 0)
        if side_number == 1:
            side.y = 1
        elif side_number == 2:
            side.x = -1
        elif side_number == 3:
            side.y = -1
        else:
            side.x = 1
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
        boundaries touch.

        Args:
            other (collider): object that may be touching self.

        Returns:
            touching (Bool): Whether self and other are touching.
        """
        return (self.parent_obj.right() >= other.parent_obj.left() and
                self.parent_obj.left() <= other.parent_obj.right() and
                self.parent_obj.top() <= other.parent_obj.bottom() and
                self.parent_obj.bottom() >= other.parent_obj.top())
