from collections import namedtuple


Operation = namedtuple('Operation', ["verb", "set"])


def read_data(fname):
    all_power_sequences = []
    for line in open(fname):
        line = line.strip()
        if not line:
            continue
        verb, sequences = line.split(' ')
        sequences = sequences.split(',')
        x, y, z = (s.split('=')[-1] for s in sequences)
        x_r, y_r, z_r = map(lambda s: tuple(int(n) for n in s.split('..')), (x, y, z))
        all_power_sequences.append(Operation(verb, (x_r, y_r, z_r)))
    return all_power_sequences


def test_read_data():
    for ifile in ('test1.txt', 'test2.txt', 'test3.txt', 'input.txt'):
        for verb, (x_seq, y_seq, z_seq) in read_data(ifile):
            assert verb in ('on', 'off')
            x1, x2 = x_seq
            y1, y2 = y_seq
            z1, z2 = z_seq
            assert x1 <= x2
            assert y1 <= y2
            assert z1 <= z2


def test_part1():
    assert part1('test1.txt') == 39
    assert part1('test2.txt') == 590784
    assert part1('test3.txt') == 474140
    assert part1('input.txt') == 545118


def part1(fname):
    lit = set()
    for verb, ((x1, x2), (y1, y2), (z1, z2)) in read_data(fname):
        x1 = max(-50, x1)
        x2 = min(50, x2)
        y1 = max(-50, y1)
        y2 = min(50, y2)
        z1 = max(-50, z1)
        z2 = min(50, z2)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if verb == 'off':
                        lit.discard((x, y, z))
                    else:
                        lit.add((x, y, z))
    return len(lit)

