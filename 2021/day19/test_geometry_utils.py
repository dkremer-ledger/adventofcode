import itertools

import pytest
from hypothesis.strategies import integers, builds, tuples, one_of
from hypothesis import given
from geometry_utils import (
    Id,
    Matrix,
    Vector,
    Tx,
    Ty,
    Tz,
    all_cubic_group_transformations,
    invert,
)


@given(integers(), integers(), integers())
def test_identity_vector_multiplication(a, b, c):
    assert Id.apply((a, b, c)) == Matrix((a, b, c))


@given(
    tuples(integers(), integers(), integers()),
    tuples(integers(), integers(), integers()),
    tuples(integers(), integers(), integers()),
)
def test_identity_matrix_multiplication(a, b, c):
    assert Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1))).multiply((a, b, c)) == Matrix(
        (a, b, c)
    )


@given(a=integers(), b=integers(), c=integers(), m=builds(lambda: Tx))
def test_rotation_along_x_axis(a, b, c, m):
    assert m.apply((a, b, c)) == (a, c, (-1) * b), f"failure {a} {b} {c}"
    assert m.multiply(m).multiply(m).multiply(m).apply((a, b, c)) == (
        a,
        b,
        c,
    ), f"failure {a} {b} {c}"


@given(a=integers(), b=integers(), c=integers(), m=builds(lambda: Ty))
def test_rotation_along_y_axis(a, b, c, m):
    assert m.apply((a, b, c)) == ((-1) * c, b, a)
    assert m.multiply(m).multiply(m).multiply(m).apply((a, b, c)) == (a, b, c)


@given(a=integers(), b=integers(), c=integers(), m=builds(lambda: Tz))
def test_rotation_along_z_axis(a, b, c, m):
    assert m.apply((a, b, c)) == (b, -a, c)
    assert m.multiply(m).multiply(m).multiply(m).apply((a, b, c)) == (a, b, c)


@given(
    integers(min_value=1, max_value=40),
    one_of(builds(lambda: Tx), builds(lambda: Ty), builds(lambda: Tz)),
    builds(lambda: Id),
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
    m1, m2, m3 = Tx, Ty, Tz
    total_set = set()
    for k, l, m in itertools.product(range(0, 20), range(0, 20), range(0, 20)):
        total_set.add((m1 ** k) * (m2 ** l) * (m3 ** m))
    assert len(total_set) == 24


@pytest.mark.parametrize("rotation", list(all_cubic_group_transformations))
def test_invert(rotation):
    assert invert(rotation) * rotation == Id
