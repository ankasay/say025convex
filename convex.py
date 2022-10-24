from cmath import inf
from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def convex_dist(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def convex_dist(self):
        inside = self.p.inside_triangle(Figure.p1, Figure.p2, Figure.p3)
        if not inside:
            return self.p.point_dist(Figure.p1, Figure.p2, Figure.p3)
        else:
            return 0.0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def convex_dist(self):
        # Одна из точек отрезка лежит внутри треугольника
        if (self.p.inside_triangle(Figure.p1, Figure.p2, Figure.p3) or
                self.q.inside_triangle(Figure.p1, Figure.p2, Figure.p3)):
            return 0.0

        # Отрезок пересекает сторону треугольника
        elif R2Point.intersect_triangle(self.p, self.q,
                                        Figure.p1,
                                        Figure.p2,
                                        Figure.p3):
            return 0.0

        else:
            return min(R2Point.dist_between_segments(self.p, self.q,
                                                     Figure.p1, Figure.p2
                                                     ),
                       R2Point.dist_between_segments(self.p, self.q,
                                                     Figure.p2, Figure.p3
                                                     ),
                       R2Point.dist_between_segments(self.p, self.q,
                                                     Figure.p3, Figure.p1
                                                     )
                       )


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()

        self.dist = {}

        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._dist = self.init_polygon_dist()

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def convex_dist(self):
        return self._dist

    def init_polygon_dist(self):
        for i in range(3):
            a = Segment(self.points.first(), self.points.last()).convex_dist()
            self.dist[frozenset((self.points.first(), self.points.last()))] = a
            self.points.push_first(self.points.pop_last())
        return min(self.dist.values())

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # Флаг, показывающий, что было удалено ребро, расстояние
            # от которого до заданного треугольника минимально
            flag = False

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            tmp = self.dist.pop(frozenset(
                                (self.points.first(), self.points.last())))
            if tmp == self._dist:
                flag = True

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())

                tmp = self.dist.pop(frozenset((p, self.points.first())))
                if not flag and tmp == self._dist:
                    flag = True

                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())

                tmp = self.dist.pop(frozenset((self.points.last(), p)))
                if not flag and tmp == self._dist:
                    flag = True

                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())

            a = Segment(t, self.points.first()).convex_dist()
            self.dist[frozenset((t, self.points.first()))] = a
            b = Segment(self.points.last(), t).convex_dist()
            self.dist[frozenset((self.points.last(), t))] = b

            if flag or a < self._dist or b < self._dist:
                self._dist = min(self.dist.values())

            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
