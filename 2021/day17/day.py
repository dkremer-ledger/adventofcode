import itertools
from typing import TypeAlias


target = (88, 125), (-157, -103)
#target = (20, 30), (-10, -5)
Velocity: TypeAlias = tuple[int, int]
Position: TypeAlias = tuple[int, int]


def step(position, velocity) -> tuple[Velocity, Position]:
    x, y = position
    vx, vy = velocity
    vx_new = vx if vx == 0 else vx + 1 if vx < 0 else vx - 1
    vy_new = vy - 1
    return (x + vx, y + vy), (vx_new, vy_new)


def reached(x, y):
    (xl, xu), (yl, yu) = target
    return xl <= x <= xu and yl <= y <= yu


def too_far(x, y):
    (xl, xu), (yl, yu) = target
    return x > xu or y < yl

possible_vx = list(range(0, 1000))
possible_vy = list(range(-3000, 3000))

max_vy = 0
max_y = 0
possible = []
for speed in itertools.product(possible_vx, possible_vy):
    position = (0, 0)
    reach = reached(*position)
    too_farr = too_far(*position)
    vx, vy = speed
    while not reach and not too_farr:
        x, y = position
        position, speed = step(position, speed)
        reach = reached(*position)
        too_farr = too_far(*position)
        
    if too_farr:
        # print(f"solution with {vx}, {vy} does not work")
        pass
    elif reach:
        possible.append(speed)
        max_vy = max(vy, max_vy)
        max_y = sum(k for k in range(max_vy + 1))
        
print(max_vy)
print(max_y)
print(len(possible))
