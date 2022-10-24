#!/usr/bin/env -S python3 -B


from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon, Figure


def get_triangle():
    flag = True
    while flag:
        print('Введите координаты вершин треугольника')
        a, b, c = R2Point(), R2Point(), R2Point()
        if R2Point.is_triangle(a, b, c):
            if b.is_light(a, c):
                Figure.p1 = c
                Figure.p3 = a
            else:
                Figure.p1 = a
                Figure.p3 = c
            Figure.p2 = b
            flag = False
        else:
            print("Заданные точки не образуют треугольник!")


def void_draw(self, tk, colour="black"):
    pass


def point_draw(self, tk, colour="black"):
    tk.draw_point(self.p, colour)


def segment_draw(self, tk, colour="black"):
    tk.draw_line(self.p, self.q, colour)


def polygon_draw(self, tk, colour="black"):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first(), colour)
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()

get_triangle()

print("Введите координаты точек выпуклой оболочки")
try:
    while True:
        tk.draw_line(Figure.p1, Figure.p2, "red")
        tk.draw_line(Figure.p2, Figure.p3, "red")
        tk.draw_line(Figure.p3, Figure.p1, "red")
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, "
              f"P = {f.perimeter()}, "
              f"D = {f.convex_dist()}\n"
              )
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
