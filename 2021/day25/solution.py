from typing import Union

import pytest


class SeaFloor(list):
    def __init__(self, input_data: Union["SeaFloor", str]):
        if isinstance(input_data, SeaFloor):
            input_data = "\n".join(''.join(row) for row in input_data)

        super().__init__(list(line.strip()) for line in input_data.splitlines())
        self.x_max = len(self[0]) - 1
        self.y_max = len(self) - 1

    def move_east(self) -> "SeaFloor":
        new_floor = SeaFloor(self)
        for line_number, row in enumerate(self):
            for position, element in enumerate(row):
                if element != '>':
                    continue
                next_position = (position + 1) % (self.x_max + 1)
                if row[next_position] == '.':
                    new_floor[line_number][next_position] = '>'
                    new_floor[line_number][position] = '.'
        return new_floor

    def move_south(self) -> "SeaFloor":
        new_floor = SeaFloor(self)
        for line_number, row in enumerate(self):
            for position, element in enumerate(row):
                if element != 'v':
                    continue
                next_position = (line_number + 1) % (self.y_max + 1)
                if self[next_position][position] == '.':
                    new_floor[next_position][position] = 'v'
                    new_floor[line_number][position] = '.'

        return new_floor

    def apply(self, n: int = 1):
        if n == 0:
            return self
        e = self.move_east()
        s = e.move_south()
        return s.apply(n - 1)

    def to_string(self):
        return "\n".join(''.join(row) for row in self)

    def __eq__(self, other):
        return self.to_string() == other.to_string()

    def solution(self):
        initial = self
        different = True
        counter = 0
        while different:
            new_one = initial.apply()
            different = new_one != initial
            initial = new_one
            counter += 1

        return counter


@pytest.fixture
def data_element_one():
    return SeaFloor("""...>...
.......
......>
v.....>
......>
.......
..vvv..""")


@pytest.fixture
def data_element_two():
    return SeaFloor("""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""")


def test_one_step(data_element_one):
    assert data_element_one == data_element_one

    assert SeaFloor(data_element_one).apply() == SeaFloor("""..vv>..
.......
>......
v.....>
>......
.......
....v..""")


def test_two_steps():
    assert SeaFloor("""..vv>..
    .......
    >......
    v.....>
    >......
    .......
    ....v..""").apply() == SeaFloor(
        """....v>.
..vv...
.>.....
......>
v>.....
.......
......."""
    )


def test_four_steps(data_element_one):
    assert data_element_one.apply(4) == SeaFloor(""">......
..v....
..>.v..
.>.v...
...>...
.......
v......""")


def test_twenty_steps(data_element_two):
    assert data_element_two.apply(20) == SeaFloor("""v>.....>>.
>vv>.....v
.>v>v.vv>>
v>>>v.>v.>
....vv>v..
.v.>>>vvv.
..v..>>vv.
v.v...>>.v
..v.....v>""")


def test_fifty_eight_steps(data_element_two):
    assert data_element_two.apply(58) == SeaFloor("""..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..""")


def test_solution(data_element_two):
    assert (data_element_two.solution()) == 58


print(SeaFloor(open('input.txt').read()).solution())
