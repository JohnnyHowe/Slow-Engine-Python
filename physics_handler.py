from .physics_objects import BoxCollider


class PhysicsHandler:
    def __init__(self, objects):
        self.objects = objects  # a REFERENCE to the objects in game_obj

    def update(self):
        self.collisions()

    def collisions(self):
        for object1 in self.objects:
            if object1.collider is not None:

                for object2 in self.objects:
                    if object2.collider is not None:

                        if object1 == object2:
                            continue

                        if type(object1.collider) == type(object2.collider) == BoxCollider:
                            if self.box_collision(object1, object2):
                                self.fix_position(object1, object2)

    def fix_position(self, object1, object2):
        """ Given two Object2ds move them so there is no overlap. This is done when there is a
        collision. """

        if object2.collider.fixed:
            object1, object2 = object2, object1

        if object1.collider.fixed:
            collision_side = object1.collider.collision_side(object2)
            print(collision_side)
            return

            if abs(movement.y) > abs(movement.x):
                object2.pos.y += overlap.y * (movement.y / abs(movement.y))
                object2.velocity.y = 0
            else:
                object2.pos.x += overlap.x * (movement.x / abs(movement.x))
                object2.velocity.x = 0
        else:
            # cry
            print("OH GOD AAAAAAAAAAAA (physics_handler.py fix_position function)")
            pass

    def box_collision(self, object1, object2):
        """ other (BoxCollider2d): box to check if self has collided with.
        Return (Bool): collision state. """
        return (object1.right() > object2.left() and
                object1.left() < object2.right() and
                object1.top() < object2.bottom() and
                object1.bottom() > object2.top())
