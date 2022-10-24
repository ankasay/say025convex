from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    def __hash__(self):
        return hash((self.x, self.y))

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    # Скалярное произведение двухмерных векторов
    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y

    def inside_triangle(self, a, b, c):
        return (self.is_light(a, b) and
                self.is_light(b, c) and self.is_light(c, a))

    # Расстояние от точки до заданного треугольника, если она лежит вне его
    def point_dist(self, a, b, c):
        return min(self.min_dist(a, b),
                   self.min_dist(b, c),
                   self.min_dist(c, a),
                   )

    # Расстояние от точки до отрезка
    def min_dist(self, a, b):
        v1 = R2Point(b.x - a.x, b.y - a.y)
        u1 = R2Point(self.x - a.x, self.y - a.y)
        v2 = R2Point(a.x - b.x, a.y - b.y)
        u2 = R2Point(self.x - b.x, self.y - b.y)

        if R2Point.dot(v1, u1) * R2Point.dot(v2, u2) < 0:
            return min(a.dist(self), b.dist(self))
        else:
            return 2 * abs(R2Point.area(self, a, b)) / a.dist(b)

    @staticmethod
    def dist_between_segments(a, b, c, d):
        return min(a.min_dist(c, d), b.min_dist(c, d),
                   c.min_dist(a, b), d.min_dist(a, b))

    @staticmethod
    def intersect_triangle(p1, p2, a, b, c):
        return (R2Point.intersect(p1, p2, a, b) or
                R2Point.intersect(p1, p2, b, c) or
                R2Point.intersect(p1, p2, c, a))

    @staticmethod
    def intersect(p1, p2, p3, p4):
        d1 = R2Point.area(p3, p4, p1)
        d2 = R2Point.area(p3, p4, p2)
        d3 = R2Point.area(p1, p2, p3)
        d4 = R2Point.area(p1, p2, p4)

        if d1 * d2 < 0 and d3 * d4 < 0:
            return True
        elif d1 == 0 and p1.is_inside(p3, p4):
            return True
        elif d2 == 0 and p2.is_inside(p3, p4):
            return True
        elif d3 == 0 and p3.is_inside(p1, p2):
            return True
        elif d4 == 0 and p4.is_inside(p1, p2):
            return True
        else:
            return False


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
