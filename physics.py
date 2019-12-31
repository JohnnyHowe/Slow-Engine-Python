from .game_display import draw_game_rect
from .geometery import *


class BoxObject:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.mass = size.x * size.y
        self.velocity = Vector(0, 0)
        self.max_velocity = Vector(float("inf"), float("inf"))

    def show_block(self, engine, color=(0, 200, 0)):
        draw_game_rect(engine.window, self.pos, self.size, color)

    def apply_velocity(self, engine):
        self.pos += self.velocity * engine.clock.dtime

    def update(self, engine):
        self.cap_velocity()
        self.apply_velocity(engine)

    def cap_velocity(self):
        self.velocity.x = min(max(-self.max_velocity.x, self.velocity.x), self.max_velocity.x)
        self.velocity.y = min(max(-self.max_velocity.y, self.velocity.y), self.max_velocity.y)

    def left(self):
        return self.pos.x - self.size.x / 2

    def right(self):
        return self.pos.x + self.size.x / 2

    def top(self):
        return self.pos.y + self.size.y / 2

    def bottom(self):
        return self.pos.y - self.size.y / 2


class BoxCollider:
    def __init__(self, parent):
        self.parent = parent

    def box_overlap(self, other):
        """ What is the size of the overlap between self and other? """
        if self.is_collided_box(other):
            return Vector(abs(min(self.parent.right(), other.parent.right()) - max(self.parent.left(), other.parent.left())),
                          abs(min(self.parent.top(), other.parent.top()) - max(self.parent.bottom(), other.parent.bottom())))
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
            if self.parent.pos.x > other.parent.pos.x:
                side.x = -side.x
            if self.parent.pos.y > other.parent.pos.y:
                side.y = -side.y
            return side
        else:
            return Vector(0, 0)

    def is_collided_box(self, other):
        """ Is there some overlap between self and other? """
        return (self.parent.left() < other.parent.right() and self.parent.right() > other.parent.left() and
                self.parent.bottom() < other.parent.top() and self.parent.top() > other.parent.bottom())

    def box_collision(self, other):
        """ If self has collided with other, move them so they aren't collided. """
        collision_side = self.box_collision_side(other)
        if collision_side.x:
            self.box_collision_rectify_x_pos(other, collision_side)
            self.box_collision_rectify_x_velocity(other)
        if collision_side.y:
            self.box_collision_rectify_y_pos(other, collision_side)
            self.box_collision_rectify_y_velocity(other)

    def box_collision_rectify_x_velocity(self, other):
        """ Assuming a collision on the x axis, rectify the positions and velocities in the x axis. """
        if self.parent.mass == other.parent.mass == float("inf"):
            raise Exception("TWO OBJECTS WITH INFINITE MASS COLLIDED WTF DO I DO.")
        elif self.parent.mass == float("inf"):
            other.parent.velocity.x = self.parent.velocity.x
        elif other.parent.mass == float("inf"):
            self.parent.velocity.x = other.parent.velocity.x
        else:
            self_momentum = self.parent.mass * self.parent.velocity.x
            other_momentum = other.parent.mass * other.parent.velocity.x
            total_momentum = self_momentum + other_momentum
            total_mass = self.parent.mass + other.parent.mass
            final_velocity = total_momentum / total_mass
            self.parent.velocity.x = final_velocity
            other.parent.velocity.x = final_velocity

    def box_collision_rectify_y_velocity(self, other):
        """ Assuming a collision on the x axis, rectify the velocity in the y axis. """
        if self.parent.mass == other.parent.mass == float("inf"):
            raise Exception("TWO OBJECTS WITH INFINITE MASS COLLIDED WTF DO I DO.")
        elif self.parent.mass == float("inf"):
            other.parent.velocity.y = self.parent.velocity.y
        elif other.parent.mass == float("inf"):
            self.parent.velocity.y = other.parent.velocity.y
        else:
            self_momentum = self.parent.mass * self.parent.velocity.y
            other_momentum = other.parent.mass * other.parent.velocity.y
            total_momentum = self_momentum + other_momentum
            total_mass = self.parent.mass + other.parent.mass
            final_velocity = total_momentum / total_mass
            self.parent.velocity.y = final_velocity
            other.parent.velocity.y = final_velocity

    def box_collision_rectify_x_pos(self, other, collision_side):
        """ Assuming a collision on the x axis, rectify the pos in the x axis. """
        self.parent.pos.x = other.parent.pos.x + collision_side.x * -1 * (other.parent.size.x + self.parent.size.x) / 2

    def box_collision_rectify_y_pos(self, other, collision_side):
        """ Assuming a collision on the x axis, rectify the pos in the y axis. """
        self.parent.pos.y = other.parent.pos.y + collision_side.y * -1 * (other.parent.size.y + self.parent.size.y) / 2


