import re
import pytest
import random

from collections import defaultdict
import itertools

from snippet1 import mx, my, mz, Matrix, all_rotations, invert, identity, Vector


def parse_file(fname):
    with open(fname) as f:
        data = f.read()
    return parse_data(data)


def parse_data(data: str):
    all_scanners_data = re.split(r"--- scanner \d+ ---", data, flags=re.MULTILINE)
    data = []
    for scanner in all_scanners_data:
        if not scanner.strip():
            continue
        data.append(
            [
                Vector(int(c) for c in l.strip().split(","))
                for l in scanner.splitlines()
                if l
            ]
        )
    return data


@pytest.fixture
def data_test():
    data = parse_file("test.txt")
    assert len(data) == 5
    return data


@pytest.fixture
def real_data():
    data = parse_file("input.txt")
    return data


def matcher(
    beacon_reference_list: set[Vector], unknown_scanner_beacon_list: set[Vector]
):
    for transformation in all_rotations():
        result = defaultdict(lambda: [])
        test_list: list[(Vector, Vector)] = [
            (beacon, transformation.apply(beacon))
            for beacon in unknown_scanner_beacon_list
        ]
        for ref_point in beacon_reference_list:
            for original_coordinates, transformed_coordinates in test_list:
                result[ref_point - transformed_coordinates].append(
                    (ref_point, original_coordinates)
                )

        for possible_translation_vector, success in sorted(
            result.items(), key=lambda args: (-1) * len(args[1])
        ):
            if len(success) < 12:
                break
            is_valid = verify(
                beacon_reference_list,
                unknown_scanner_beacon_list,
                possible_translation_vector,
                transformation,
            )
            if is_valid:
                return is_valid


def verify(beacon_source, other_beacons, translation, rotation):
    translated_beacons = set(rotation.apply(b) + translation for b in other_beacons)
    if len(translated_beacons.intersection(set(beacon_source))) < 12:
        return False
    return translation, rotation


def test_match_scanner_1_and_scanner_2(data_test):
    result = matcher(data_test[0], data_test[1])
    assert result
    translation, rotation = result
    data_test_source = set(data_test[0])
    data_test_remote = set(data_test[1])
    transformed_remote = set(rotation.apply(b) + translation for b in data_test_remote)
    assert (
        len(
            set(data_test[0]).intersection(
                set((rotation.apply(b) + translation) for b in data_test[1])
            )
        )
        == 12
    )


def full_beacon_list(data_):
    all_data = {k: d for k, d in enumerate(data_)}
    studied = {}
    to_study = [(0, data_[0])]
    non_reached = [(k, d) for k, d in enumerate(data_[1:], 1)]
    all_pos = {0: (0, 0, 0)}
    while non_reached:
        index, source = to_study.pop()
        for indexp, scanner in non_reached:
            if r := matcher(set(source), set(scanner)):
                tr, rot = r
                to_study.append(
                    (indexp, set(Vector(rot.apply(b) + tr) for b in scanner))
                )
                all_pos[indexp] = tr
        assert index not in studied
        studied[index] = source
        non_reached = [
            (k, v) for (k, v) in non_reached if k not in set(l for (l, w) in to_study)
        ]

    all_beacons = set()
    assert len(studied) + len(to_study) == len(all_data)
    assert len(all_pos) == len(all_data)

    for k, data in to_study:
        for b in data:
            all_beacons.add(b)
    for k, steps in studied.items():
        for b in steps:
            all_beacons.add(b)
    return all_beacons, all_pos


def max_manhattan_between_scanners(positions):
    d_max = 0
    for (s1, pos1), (s2, pos2) in itertools.product(
        positions.items(), positions.items()
    ):
        d_max = max(d_max, sum(abs(u - v) for u, v in zip(pos1, pos2)))
    return d_max


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


@pytest.mark.parametrize("rotation", list(all_rotations()))
def test_matcher(rotation):
    initial_source = {
        Vector(
            (random.randint(0, 1000), random.randint(0, 999), random.randint(0, 999))
        )
        for x in range(30)
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
