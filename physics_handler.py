from .physics_objects import BoxCollider


class PhysicsHandler:
    def __init__(self, objects):
        self.objects = objects  # a REFERENCE to the objects in game_obj

    def update(self, game_obj):
        pass

    def fix_position(self, object1, object2):
        pass


