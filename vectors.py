""" Module containing vectors to be used for size and positions. """
from math import sqrt


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        """ Return length of vector (sqrt(x^2 + y^2))"""
        return sqrt(self.x ** 2 + self.y ** 2)

    def copy(self):
        """ Return a copy of self. """
        return Vector(self.x, self.y)

    def tuple(self):
        """ Return a tuple of the vector as (x, y) """
        return self.x, self.y

    def __str__(self):
        rounding_dp = 2
        return "Vector({}, {})".format(str(round(self.x, rounding_dp)), str(round(self.y, rounding_dp)))

    def __iter__(self):
        for item in [self.x, self.y]:
            yield item

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

