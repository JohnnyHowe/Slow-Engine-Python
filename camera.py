from slowEngine.vector2 import Vector2
from slowEngine.display import Display


class _Camera:

    position = None
    size = None

    def __init__(self):
        self.position = Vector2(0, 0)
        self.size = 10

    def world_to_display_position(self, world_position):
        """ Where on the screen should the world position be shown? """
        offset = Display.size / 2 + self.position
        return Vector2(world_position.x, -world_position.y) * self.get_display_size() + offset

    def get_display_size(self):
        return min(Display.size) / self.size


Camera = _Camera()
