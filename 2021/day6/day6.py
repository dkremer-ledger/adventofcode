from typing import TypeAlias, List
from collections import Counter

import pytest

Board: TypeAlias = List


@pytest.fixture
def input_data():
    return Counter(map(int, open('day6.txt').read().split(',')))


def evolve_pop(pop):
    new_pop = Counter()
    for key, value in pop.items():
        if key == 0:
            new_pop[8] += value
            new_pop[6] += value
            continue
        new_pop[key - 1] += pop[key]
    return new_pop


def evolve(pop, n: int = 80):
    for day in range(n):
        pop = evolve_pop(pop)
    return sum(pop.values())


def test_part_1(input_data):
    assert evolve(input_data, 80) == 374927


def test_part_2(input_data):
    assert evolve(input_data, 256) == 1687617803407

