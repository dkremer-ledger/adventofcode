data = [
list(map(int, l.strip())) for l in """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines()]

data = [list(map(int, l.strip())) for l in open('input.txt')]

X_MAX = len(data[0])
Y_MAX = len(data)

def neighbours(x, y):
    for u in range(x - 1, x +2):
        for v in range(y - 1, y + 2):
            if (u, v) == (x, y):
                continue
            if u < 0 or v < 0:
                continue
            if u >= X_MAX or v >= Y_MAX:
                continue
            yield u, v


print(list(neighbours(1,1)))
assert len(list(neighbours(1, 1))) == 8

def increase_by_one(data):
    return [[octo + 1 for octo in row] for row in data] 

def do_flash(data, x, y):
    for (u, v) in neighbours(x, y):
        data[v][u] += 1


def flash_octopuses(data, flashed=None):
    flashed = set() if flashed is None else flashed
    for y, row in enumerate(data):
        for x, octopus in enumerate(row):
            if octopus > 9 and (x, y) not in flashed:
                flashed.add((x, y))
                do_flash(data, x, y)
    return data

    
def step(data):
    flashed = set()
    initial_flashed = None
    for y, row in enumerate(data):
        for x, octopus in enumerate(row):
            data[y][x] += 1
    while initial_flashed != flashed:
        initial_flashed = set(flashed)
        flash_octopuses(data, flashed)
    for (x, y) in flashed:
        data[y][x] = 0
    print("\n".join("".join(str(x) if x != 0 else ' ' for x in row)for row in data))
    print()
    return data, len(flashed)

total_flashes = 0

for k in range(10000):
    data, n_flashes = step(data)
    if n_flashes == X_MAX * Y_MAX:
        print("step",k+1)
        break
    total_flashes += n_flashes

print(total_flashes)
