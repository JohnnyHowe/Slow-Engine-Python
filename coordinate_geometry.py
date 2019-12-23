from .vectors import Vector


class Line:
    def __init__(self, start, end):
        self.pos1 = start
        self.pos2 = end

    def line_intersection(self, other):
        """ Return the vector position of the intersection of self and other. """
        x1, y1 = self.pos1.tuple()
        x2, y2 = self.pos2.tuple()
        x3, y3 = other.pos1.tuple()
        x4, y4 = other.pos2.tuple()

        x_pos_numerator = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        x_pos_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        y_pos_numerator = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        y_pos_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if x_pos_denominator and y_pos_denominator:
            pos = Vector(x_pos_numerator / x_pos_denominator, y_pos_numerator / y_pos_denominator)
        else:
            pos = Vector(0, 0)
        return pos

    def box_intersections(self, other):
        """ Where does self and other intersect?

        Args:
            other (BoxCollider): The object to detect the intersection on.

        Returns:
            if self and other intersects:
                positions (list): positions of intersection (on edge of object) and the side of the object.
            else:
                False
        """
        obj_borders = other.border_lines()
        intersections = []
        for border, side in obj_borders:
            pos = self.line_intersection(border)

            if border.pos1.y == border.pos2.y:
                in_border_range = True
            else:
                in_border_range = border.pos1.y <= pos.y <= border.pos2.y or border.pos2.y <= pos.y <= border.pos1.y
            if border.pos1.x == border.pos2.x:
                in_border_domain = True
            else:
                in_border_domain = border.pos1.x <= pos.x <= border.pos2.x or border.pos2.x <= pos.x <= border.pos1.x

            if in_border_range and in_border_domain:
                intersections.append((pos, side))
        return intersections

    def __str__(self):
        return "Line({}, {})".format(self.pos1.tuple(), self.pos2.tuple())

    def __repr__(self):
        return self.__str__()
