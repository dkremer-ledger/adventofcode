import statistics as stats


crabs = list(map(int, open('input.txt').read().split(',')))


def part2(crab_list):
    """
    Instead of optimizing the difference with the target,
    We optimize the quadratic difference with the target
    We try all possible solution in the range (0, 1000), this just works.
    A true least-square optimization algorithm would work too but let's be lazy for this one.
    """
    def fuel(target, crab_position):
        d = abs(target - crab_position)
        return ((d + 1) * d) // 2

    def total_fuel(target, crab_list_):
        return sum(fuel(target, crab) for crab in crab_list)

    result = min(
        (
            (target, total_fuel(target, crab_list)) for target in range(0, 1000)
        ), key=lambda x: x[1]
    )
    return result[1]  # this is the total fuel used


def part1(crab_list):
    median = round(stats.median(crabs))
    total_fuel = sum(abs(x - median) for x in crab_list)
    print(
        "part1; ideal position is median of all crab's positions; median={}, fuel={}",
        median, total_fuel
    )
    return total_fuel


def test_solution_part1():
    assert part1(crabs) == 343605


def test_solution_part2():
    assert part2(crabs) == 96744904
