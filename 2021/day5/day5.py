from dataclasses import dataclass
from collections import Counter


raw_data = open('day5.txt').read()
all_segments = []
xmax = 0
ymax = 0
for line in raw_data.splitlines():
    a, b = line.split(' -> ')
    x, y = map(int, a.split(','))
    xp, yp = map(int, b.split(','))
    xmax = max(x, xp, xmax)
    ymax = max(y, yp, ymax)
    all_segments.append(((x, y), (xp, yp)))


MAP = [([0] * 991) for _ in range(991)]
print("### PART 1 ###")
for ((x, y), (xp, yp)) in all_segments:
    if x != xp and y != yp:
        continue
    elif y == yp:
        for abs_ in range(min(x, xp), max(x,xp) + 1):
            MAP[y][abs_] += 1
    elif x == xp:
        for ord_ in range(min(y, yp), max(y, yp) + 1):
            MAP[ord_][x] += 1
    elif x == xp and y == yp:
        MAP[y][x] += 1
    else:
        raise ValueError()

print("xmax, ymax=", (xmax, ymax))
print("number of points", sum(sum(1 for x in row if x > 1) for row in MAP))
print("### PART 2 ###")
MAP = [([0] * 991) for _ in range(991)]
for ((x, y), (xp, yp)) in all_segments:
    if x != xp and y != yp:
        dy = -1 if yp < y else 1
        dx = -1 if xp < x else 1
        cur_x, cur_y = x, y
        MAP[cur_y][cur_x] += 1
        while (cur_x, cur_y) != (xp, yp):
            cur_x += dx
            cur_y += dy
            MAP[cur_y][cur_x] += 1
    elif y == yp:
        for abs_ in range(min(x, xp), max(x,xp) + 1):
            MAP[y][abs_] += 1
    elif x == xp:
        for ord_ in range(min(y, yp), max(y, yp) + 1):
            MAP[ord_][x] += 1
    elif x == xp and y == yp:
        MAP[y][x] += 1
    else:
        raise ValueError()

print("xmax, ymax=", (xmax, ymax))
print("number of points", sum(sum(1 for x in row if x > 1) for row in MAP))
