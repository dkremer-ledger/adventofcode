import random

import pytest

from day19 import full_beacon_list, matcher, max_manhattan_between_scanners, verify
from geometry_utils import Vector, all_cubic_group_transformations, invert
from helpers import parse_file


@pytest.fixture
def data_test():
    data = parse_file("test.txt")
    assert len(data) == 5
    return data


@pytest.fixture
def real_data():
    data = parse_file("input.txt")
    return data


def test_match_scanner_1_and_scanner_2(data_test):
    result = matcher(data_test[0], data_test[1])
    assert result
    translation, rotation = result
    assert (
        len(
            set(data_test[0]).intersection(
                set((rotation.apply(b) + translation) for b in data_test[1])
            )
        )
        == 12
    )


def test_full_beacon_list(data_test):
    all_beacons, all_pos = full_beacon_list(data_test)
    assert len(all_beacons) == 79
    assert max_manhattan_between_scanners(all_pos) == 3621


def test_with_real_data(real_data):
    all_beacons, positions = full_beacon_list(real_data)
    print("number of beacons:", len(all_beacons))
    assert len(all_beacons) == 405
    d_max = max_manhattan_between_scanners(positions)
    print(d_max)


@pytest.mark.parametrize("rotation", list(all_cubic_group_transformations))
def test_matcher(rotation):
    initial_source = {
        Vector(
            (random.randint(0, 1000), random.randint(0, 999), random.randint(0, 999))
        )
        for _ in range(30)
    }
    translation_vector = Vector((345, 789, 123))
    other_beacon = {rotation.apply(b + translation_vector) for b in initial_source}
    tr, rot = verify(
        initial_source,
        other_beacon,
        Vector((-1) * v for v in translation_vector),
        invert(rotation),
    )
    assert tr, rot == matcher(initial_source, other_beacon)
