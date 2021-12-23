
mat = []
with open('input') as f:
    for line in f:
        mat.append(list(map(int, line.strip())))


# mat = [list(map(int, row.strip())) for row in """2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678""".splitlines()]

MAX_X = len(mat[-1]) - 1
MAX_Y = len(mat) - 1

def print_pool(pool):
    mymat = [row[:] for row in mat]        
    for y, row in enumerate(mymat):
        for x, col in enumerate(row):
            if (y, x) not in pool:
                mymat[y][x] = ' '
            else:
                mymat[y][x] = str(mymat[y][x])
    print("\n".join("".join(row) for row in mymat))

def neighbours(y, x):
    output = []
    for u, v in [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]:
        if u < 0 or v < 0 or u > MAX_Y or v > MAX_X:
            continue
        output.append((u, v))
        
    return output

def find_pool(lowest_point, seen=None):
    seen = set() if seen is None else seen
    seen.add(lowest_point)
    ly, lx = lowest_point
    neighs = [neigh for neigh in neighbours(*lowest_point) if neigh not in seen]
    neighs_to_explore = [(y, x) for (y, x) in neighs if mat[y][x] > mat[ly][lx]]
    for u, v in neighs_to_explore:
        if mat[u][v] == 9:
            continue
        find_pool((u, v), seen=seen)

    return seen

print(MAX_X, MAX_Y)
lowest_points = []
output = 0
for y, row in enumerate(mat):
    for x, col in enumerate(row):
        print(f"pos: y={y}, x={x}")
        neighs = neighbours(y, x)
        if all(mat[y][x] < mat[u][v] for (u, v) in neighs):
            lowest_points.append((y, x))
            print("lower point:", col, neighs)
            output += (col + 1)

#assert output == 591
print(output)

pool_0 = find_pool(lowest_points[0])
all_pools = sorted((find_pool(p) for p in lowest_points), key=lambda x: len(x), reverse=True)      
print(len(all_pools[0]) * len(all_pools[1]) * len(all_pools[2]))
