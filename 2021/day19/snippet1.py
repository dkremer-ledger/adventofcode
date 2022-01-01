import itertools
import pytest
from hypothesis.strategies import integers, tuples, builds, one_of
from hypothesis import given


class Vector(tuple):
    def __sub__(self, other):
        return tuple(u - up for (u, up) in zip(self, other))

    def __add__(self, other):
        return tuple(u + up for (u, up) in zip(self, other))


class Matrix(tuple):
    """
    The Matrix class should in theory work for matrix in the broadest sense:
    Vectors are matrix as well but with dimension 1 instead of dimension 2 for square matrix.
    However we treat vectors as simple tuples for the sake of simplicity.
    """

    def apply(self, vec: Vector):
        return Vector(sum(l * v for l, v in zip(row, vec)) for row in self)

    def multiply(self, mat):
        return Matrix(zip(*tuple(self.apply(column) for column in zip(*mat))))

    def __mul__(self, other):
        return self.multiply(other)

    def __pow__(self, exponent: int):
        if not isinstance(exponent, int) or exponent < 0 or exponent > 99:
            raise ValueError("exponent must be an integer in range [0, 100[")
        if exponent == 0:
            return Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))

        m = Matrix(self)
        for k in range(exponent - 1):
            m = m * self
        return m


def mx():
    return Matrix(((1, 0, 0), (0, 0, 1), (0, -1, 0)))


def my():
    return Matrix(((0, 0, -1), (0, 1, 0), (1, 0, 0)))


def mz():
    return Matrix(((0, 1, 0), (-1, 0, 0), (0, 0, 1)))


def identity():
    return Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))


def invert(matrix: Matrix):
    Id, m1, m2, m3 = identity(), mx(), my(), mz()
    for k, l, m in itertools.product(range(0, 4), range(0, 4), range(0, 4)):
        inverse = (m1 ** k) * (m2 ** l) * (m3 ** m)
        if (inverse * matrix) == Id:
            return inverse
    raise ValueError(
        f"Could not invert matrix {m}: maybe it is not an element of the group?"
    )


@given(integers(), integers(), integers(), builds(identity))
def test_identity_vector_multiplication(a, b, c, m):
    m.apply((a, b, c)) == Matrix((a, b, c))


@given(
    tuples(integers(), integers(), integers()),
    tuples(integers(), integers(), integers()),
    tuples(integers(), integers(), integers()),
)
def test_identity_matrix_multiplication(a, b, c):
    assert Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1))).multiply((a, b, c)) == Matrix(
        (a, b, c)
    )


@given(a=integers(), b=integers(), c=integers(), m=builds(mx))
def test_rotation_along_x_axis(a, b, c, m):
    assert m.apply((a, b, c)) == (a, c, (-1) * b), f"failure {a} {b} {c}"
    assert m.multiply(m).multiply(m).multiply(m).apply((a, b, c)) == (
        a,
        b,
        c,
    ), f"failure {a} {b} {c}"


@given(a=integers(), b=integers(), c=integers(), m=builds(my))
def test_rotation_along_y_axis(a, b, c, m):
    assert m.apply((a, b, c)) == ((-1) * b, a, c)
    assert m.multiply(m).multiply(m).multiply(m).apply((a, b, c)) == (a, b, c)


@given(a=integers(), b=integers(), c=integers(), m=builds(mz))
def test_rotation_along_z_axis(a, b, c, m):
    assert m.apply((a, b, c)) == ((-1) * c, b, a)
    assert m.multiply(m).multiply(m).multiply(m).apply((a, b, c)) == (a, b, c)


@given(
    integers(min_value=1, max_value=40),
    one_of(builds(mx), builds(my), builds(mz)),
    builds(identity),
)
def test_rotation_modulo_4_is_identity(a, m, id_):
    if a % 4 == 0:
        assert m ** a == id_

    if a % 4 == 1:
        assert m ** a == m

    if a % 4 == 2:
        assert m ** a == (m * m)
        assert m ** a == m ** 2

    if a % 4 == 3:
        assert m ** a == (m ** 2) * m
        assert m ** a == m * (m ** 2)
        assert m ** a == m * m * m


@given(integers(), integers(), integers())
def test_vector_addition(a, b, c):
    assert Vector((1, 2, 3)) + Vector((a, b, c)) == (1 + a, 2 + b, 3 + c)


def test_possible_rotation_set_size_is_24():
    # not a proof but good enough
    m1, m2, m3 = mx(), my(), mz()
    total_set = set()
    for k, l, m in itertools.product(range(0, 20), range(0, 20), range(0, 20)):
        total_set.add((m1 ** k) * (m2 ** l) * (m3 ** m))
    assert len(total_set) == 24


def test_all_rotations():
    assert len(all_rotations()) == 24


def all_rotations():
    rotation_set = set()
    m1, m2, m3 = mx(), my(), mz()
    for k, l, m in itertools.product(range(1, 5), range(1, 5), range(1, 5)):
        rotation_set.add(m1 ** k * m2 ** l * m3 ** m)
    return rotation_set


def test_invert():
    for rotation in all_rotations():
        assert invert(rotation) * rotation == identity()
