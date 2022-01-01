from collections import defaultdict
import itertools

from geometry_utils import Vector, all_cubic_group_transformations


def matcher(
    beacon_reference_list: set[Vector], unknown_scanner_beacon_list: set[Vector]
):
    """
    Try to match a list of beacon coordinates expressed in a given reference frame
    with a list of beacon coordinates expressed in another reference frame.

    The algorithm executes as follow:

    For all transformations of the cubic group
      | Apply the transformation to the second list of beacons
      | Build the translation vector for the cartesian product of the first list with the second list
      |
    """
    for transformation in all_cubic_group_transformations:
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
            if is_valid := verify(
                beacon_reference_list,
                unknown_scanner_beacon_list,
                possible_translation_vector,
                transformation,
            ):
                return is_valid


def verify(beacon_source, other_beacons, translation, rotation):
    translated_beacons = set(rotation.apply(b) + translation for b in other_beacons)
    if len(translated_beacons.intersection(set(beacon_source))) < 12:
        return None
    return translation, rotation


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
