#!/usr/bin/env -S python3 -B


from r2point import R2Point
from convex import Void
from run_tk_convex import get_triangle

f = Void()

get_triangle()

print("Введите координаты точек выпуклой оболочки")
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, "
              f"P = {f.perimeter()}, "
              f"D = {f.convex_dist}\n"
              )
except(EOFError, KeyboardInterrupt):
    print("\nStop")
