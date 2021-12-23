import sys

sys.setrecursionlimit(10000)

from part1 import read_data


def test_part21():
    assert part2_recursive("test1.txt") == 39


def test_part22():
    assert part2_recursive("test3.txt") == 2758514936282235


def test_part23():
    assert part2_recursive("input.txt") == 1227298136842375


def point_in_segment(x: int, s: tuple[int, int]):
    x1, x2 = s
    return x1 <= x <= x2


def segment_intersection(segment1, segment2):
    segment1, segment2 = sorted([segment1, segment2])
    x1, y1 = segment1
    x2, y2 = segment2

    if not point_in_segment(x2, segment1) and not (point_in_segment(y2, segment1)):
        return None

    if y1 == y2:
        return (x2, y2)
    elif y1 < y2:
        return x2, y1
    elif y1 > y2:
        return x2, y2
    else:
        raise ValueError("unknown case")


def intersection(cube1, cube2):
    intersections = [segment_intersection(s1, s2) for s1, s2 in zip(cube1, cube2)]
    if not all(intersections):
        return EmptyCube()
    return Cube(tuple(intersections))


def area(cube):
    (x1, x2), (y1, y2), (z1, z2) = cube
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


class Expression:
    def __init__(self, lhs=None, rhs=None, depth=0):
        self.lhs = lhs or EmptyCube()
        self.rhs = rhs or EmptyCube()
        self.depth = depth

    def __str__(self):
        return f"( {self.lhs} {self.op} {self.rhs} )"


class EmptyCube:
    def __str__(self):
        return "E"

    def area(self):
        return 0

    def intersect(self, other):
        return EmptyCube()

    def union(self, other):
        return other


class Cube(tuple):
    def area(self):
        return area(self)

    def intersect(self, other):
        if isinstance(other, Cube):
            return intersection(self, other)
        elif isinstance(other, Exclude):
            return Exclude(self.intersect(other.lhs), self.intersect(other.rhs))
        elif isinstance(other, Union):
            return Union(self.intersect(other.lhs), self.intersect(other.rhs))
        elif isinstance(other, EmptyCube):
            return other
        else:
            raise NotImplementedError()

    def __str__(self):
        return "Cube"


class Exclude(Expression):
    op = "\\"

    def area(self):
        return self.lhs.area() - self.lhs.intersect(self.rhs).area()

    def intersect(self, other):
        if isinstance(other, Cube):
            return Exclude(self.lhs.intersect(other), self.rhs.intersect(other))
        elif isinstance(other, EmptyCube):
            return other
        else:
            raise NotImplementedError()


class Union(Expression):
    op = "U"

    def area(self):
        lhs_area = self.lhs.area()
        rhs_area = self.rhs.area()
        intersect_area = self.lhs.intersect(self.rhs).area()
        result = lhs_area + rhs_area - intersect_area
        return result

    def intersect(self, other):
        if isinstance(other, Cube):
            return Union(other.intersect(self.lhs), other.intersect(self.rhs))
        elif isinstance(other, EmptyCube):
            return other
        else:
            raise NotImplementedError()


def build_expression(data_list, expression=None, depth=0):
    if not data_list:
        return expression

    op = data_list.pop()
    if op.verb == "on":
        return Union(
            Cube(op.set),
            build_expression(data_list, expression, depth=depth + 1),
            depth=depth,
        )
    elif op.verb == "off":
        return Exclude(
            build_expression(data_list, expression, depth=depth + 1),
            Cube(op.set),
            depth=depth,
        )
    else:
        raise ValueError()


def part2_recursive(fname):
    data = list(read_data(fname))
    expression = build_expression(data, expression=EmptyCube())
    print("Full expression:", str(expression))
    area = expression.area()
    print(area)
    return area
