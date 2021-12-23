from typing import TypeAlias, List
from collections import Counter
Board: TypeAlias = List

pop = Counter(map(int, open('day6.txt').read().split(',')))
def evolve_pop(pop):
    new_pop = Counter()
    new_fishes = 0
    for key, value in pop.items():
        if key == 0:
            new_pop[8] += value
            new_pop[6] += value
        else:
            new_pop[key - 1] += pop[key]
    return new_pop

for day in range(256):
    pop = evolve_pop(pop)


print(sum(pop.values()))

print("### PART 1 ###")
print("### PART 2 ###")
