import math


class Vector:
    """ A 2D vector, to be used for positions, sizes, anything with an x and y value. """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def copy(self):
        """ Return a copy of self. """
        return Vector(self.x, self.y)

    def __iter__(self):
        for value in [self.x, self.y]:
            yield value

    def __round__(self, n=None):
        """ Return a vector where the values are all rounded. """
        return Vector(round(self.x, n), round(self.y, n))

    def __truediv__(self, n):
        """ Return a copy of self where the values are divided by n. """
        return Vector(self.x / n, self.y / n)

    def __mul__(self, n):
        """ Return a copy of self where the values are multiplied by n. """
        return Vector(self.x * n, self.y * n)

    def __add__(self, other):
        """ Return a vector where the values are the sum of the corresponding values of self and other. """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """ Return a vector where the values are the difference between the corresponding values of self and other. """
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def pos(self):
        return Vector(self.x, self.y)

    def size(self):
        return Vector(self.w, self.h)

    def set_pos(self, pos):
        self.x = pos.x
        self.y = pos.y

    def set_size(self, size):
        self.w = size.x
        self.h = size.y

    def left(self):
        return self.x - self.w / 2

    def right(self):
        return self.x + self.w / 2

    def top(self):
        return self.y + self.h / 2

    def bottom(self):
        return self.y - self.h / 2

    def corners(self):
        return [(self.left(), self.top()), (self.right(), self.top()),
                (self.right(), self.bottom(), self.left(), self.bottom())]

    def __mul__(self, n):
        return Rect(self.x * n, self.y * n, self.w * n, self.h * n)

    def __round__(self, n=1):
        return Rect(round(self.x, n), round(self.y, n), round(self.w, n), round(self.h, n), )

    def __iter__(self):
        for value in [self.x, self.y, self.w, self.h]:
            yield value

    def __str__(self, n=16):
        return "Rect{}".format(str(tuple(round(self, n))))

    def __repr__(self, n=1):
        self.__str__(n=16)


def new_rect(rect_tuple):
    return Rect(rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3])


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end



