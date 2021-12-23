import statistics as stats
import math
from typing import TypeAlias, List


crabs = list(map(int, open('input.txt').read().split(',')))
mean = round(stats.mean(crabs))
median = round(stats.median(crabs))
print("mean: ", mean, sum(abs(x-mean) for x in crabs))
print("median: ", median, sum(abs(x-median) for x in crabs))

def fuel_2(target, crab_position):
    d = abs(target - crab_position)
    return ((d + 1) * d) // 2

def total_fuel_2(target, crab_list):
    return sum(diff_sum(target, crab) for crab in crab_list)

r = [(target, total_fuel_2(target, crabs)) for target in range(0, 1000)]
print(min(r, key=lambda x: x[1]))
