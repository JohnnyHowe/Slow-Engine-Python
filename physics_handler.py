from .physics_objects import BoxCollider


class PhysicsHandler:
    def __init__(self, objects):
        self.objects = objects  # a REFERENCE to the objects in game_obj

    def update(self, game_obj):
        self.collider_updates(game_obj)

    def collider_updates(self, game_obj):
        for object1 in self.objects:
            if object1.collider is not None:

                for object2 in self.objects:
                    if object2.collider is not None:

                        if object1 == object2:
                            continue

                        self.collisions(object1, object2)
                        # self.apply_friction(game_obj, object1, object2)

    def apply_friction(self, game_obj, object1, object2):
        object1.apply_friction(game_obj, object2)

    def collisions(self, object1, object2):
        if type(object1.collider) == type(object2.collider) == BoxCollider:
            if object1.collider.collided_with(object2.collider):
                self.fix_position(object1, object2)

    def fix_position(self, object1, object2):
        """ Given two Object2ds move them so there is no overlap. This is done when there is a
        collision. """
        if object2.collider.fixed:
            object1, object2 = object2, object1

        if object1.collider.fixed:
            collision_side = object2.collider.box_collision_side(object1.collider)
            overlap = object2.collider.overlap(object1.collider)

            object2.pos.x -= collision_side.x * overlap.x
            object2.pos.y -= collision_side.y * overlap.y

            object2.velocity.x *= int(0 == collision_side.x)
            object2.velocity.y *= int(0 == collision_side.y)

        else:
            # cry
            print("OH GOD AAAAAAAAAAAA (physics_handler.py fix_position function)")
            pass


