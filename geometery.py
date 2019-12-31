

class Vector:
    """ A 2D vector, to be used for positions, sizes, anything with an x and y value. """
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
