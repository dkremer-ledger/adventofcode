from collections import defaultdict
from pprint import pprint
fname = 'test.txt'
fname = 'test2.txt'
fname = 'input.txt'

data = [l.strip().split('-') for l in open(fname)]

def do_map(data):
    output_map = defaultdict(lambda: set())
    for node_a, node_b in data:
        output_map[node_a].add(node_b)
        output_map[node_b].add(node_a)
    return output_map


class CaveSequence(tuple):
    def __init__(self, iterable, visited_twice=False):
        self.visited_twice = visited_twice
        super().__init__()


def cave_belong_to_path(cave, path):
    if not cave.islower():
        return False
    try:
        current, following = path
    except ValueError:
        return path[0] == cave
    else:
        if current == cave:
            return True
        return cave_belong_to_path(cave, following)


def can_visit_cave(cave, path):
    """For Part 1"""
    if not cave.islower() or not cave_belong_to_path(cave, path):
        return CaveSequence((cave, path))
    

def can_visit_cave(cave, path):
    """For Part 2"""
    if cave == 'start':
        return
        
    if cave.islower():
        if cave_belong_to_path(cave, path):
            if path.visited_twice:
                return False
            return CaveSequence((cave, path), visited_twice=cave)
    
    return CaveSequence((cave, path), visited_twice=path.visited_twice)


def do_paths(input_map, current_path = CaveSequence(('start',)), output=None):
    if current_path[0] == 'end':
        output.append(current_path)
        return

    for next_cave in input_map[current_path[0]]:        
        next_sequence = can_visit_cave(next_cave, current_path)
        if not next_sequence:
            continue
        do_paths(
            input_map,
            next_sequence,
            output
        )
    return output


print(do_map(data))
result = do_paths(do_map(data), output=[])
#pprint(result)
print(f"number of paths for {fname}:", len(result))

