""" Module containing vectors to be used for size and positions. """


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        rounding_dp = 2
        return "Vector2d({}, {})".format(str(round(self.x, rounding_dp)), str(round(self.y, rounding_dp)))

    def __iter__(self):
        for item in [self.x, self.y]:
            yield item

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

