input_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

input_data = open('input').read()


def get_input(data: str):
    part_one, part_two = data.split("\n\n")
    part_one = set(tuple(map(int, line.strip().split(','))) for line in part_one.splitlines())
    return part_one, list(l.strip().split()[-1] for l in part_two.splitlines())


p1, p2 = get_input(input_data)

max_x = max(x for (x, _) in p1)
max_y = max(y for (_, y) in p1)

print(max_x, max_y)

data = [['.' if (x, y) not in p1 else '#' for x in range(max_x+1)] for y in range(max_y+1)]


def fold_along_x(data, offset):
    folded_data = [row[offset + 1:] for row in data]
    existing_part = [row[:offset] for row in data]
    for y, (folded_row, row) in enumerate(zip(folded_data, existing_part)):
        for x, folded_dot in enumerate(folded_row[:], 1):
            if folded_dot == '#':
                existing_part[y][offset - x] = '#'
    return existing_part


def fold_along_y(data, offset):
    folded_data = data[offset + 1:]
    part = data[:offset]
    for y, folded_row in enumerate(folded_data, 1):
        for x, folded_dot in enumerate(folded_row):
            if folded_dot == '#':
                part[offset - y][x] = '#'
    return part


def count_dots(data):
    output = 0
    for row in data:
        output += row.count('#')
    return output


def print_mat(data):
    print("\n".join("".join(row) for row in data))


apply = {'y': fold_along_y, 'x': fold_along_x}

for instruction in p2:
    print_mat(data)
    print("dots: ", count_dots(data))
    print()
    axis, offset = instruction.split('=')
    data = apply[axis](data, int(offset))

print_mat(data)
print("dots: ", count_dots(data))

