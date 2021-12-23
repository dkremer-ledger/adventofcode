from collections import Counter
from pprint import pprint
fname = 'test.txt'
fname = 'input.txt'

part1, part2 = open(fname).read().split("\n\n")
polymer = part1
sequence = dict([(pair, element) for (pair, element) in map(lambda l: l.strip().split(' -> '), part2.splitlines())])
pprint(sequence)

print("Number of possible pairs", len(sequence))
print("Number of tokens", len(all_tokens))
print(polymer)


pair_mapping = {pair: (pair[0] + elem, elem + pair[1]) for pair, elem in sequence.items()}


def make_pairs(sequence: str):
    return [a + b for a, b in zip(sequence, sequence[1:])]

def answer(counter: Counter):
    sorted_elems = counter.most_common()
    print("total number of elems:", sum(counter.values()))
    print(sorted_elems)
    print("supposed answer", sorted_elems[0][1] - sorted_elems[-1][1])


def solve(initial_sequence, iterate=10):
    all_counters = []
    element_counter = Counter(initial_sequence)
    pair_counter = Counter(make_pairs(initial_sequence))
    for k in range(iterate):
        new_pair_counter = Counter()
        for pair, counter in pair_counter.items():
            pair1, pair2 = pair_mapping[pair]
            new_pair_counter[pair1] += counter
            new_pair_counter[pair2] += counter
            element_counter[sequence[pair]] += counter
        pair_counter = new_pair_counter
        answer(element_counter)
    return element_counter

solve(polymer, 40)
