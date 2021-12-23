from collections import Counter
from functools import cached_property
from pprint import pprint
import sys
import heapq

fname = 'input.txt'

class Matrix(list):
    @cached_property
    def MAX_X(self):
        return len(self[-1]) - 1

    @cached_property
    def MAX_Y(self):
        return len(self) - 1
        
    def __call__(self, x, y):
        return self[y][x]

    def neighbours(self, x, y):
        for u, v in [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]:
            if u < 0 or v < 0 or u > self.MAX_Y or v > self.MAX_X:
                continue
            yield (v, u)

mat = Matrix()

with open(fname) as f:
    for line in f:
        if not line.strip():
            continue
        mat.append(list(map(int, line.strip())))


def new_mat(matt):
    n_mat = [[0] * (len(matt[0]) * 5) for _ in range(len(matt) * 5)]
    for k, row in enumerate(n_mat):
        for l, value in enumerate(row):
            x_o = l % (matt.MAX_X + 1)
            y_o = k % (matt.MAX_Y + 1)
            x_inc = l // (matt.MAX_X + 1)
            y_inc = k // (matt.MAX_Y + 1)
            new_val = matt[y_o][x_o] + x_inc + y_inc
            n_mat[k][l] = (new_val % 9) if new_val != 9 else 9
            
    print(len(n_mat))
    return Matrix(n_mat)

## Djikstra
def visit_node(start, arrival, matrix, visited_nodes):
    new_value = visited_nodes[start] + matrix(*arrival)
    if arrival not in visited_nodes:
        visited_nodes[arrival] = new_value
    elif new_value <= visited_nodes[arrival]:
        visited_nodes[arrival] = new_value
    else:
        return
    for neigh in sorted(matrix.neighbours(*arrival), key=lambda foo: matrix(*foo)):
        visit_node(arrival, neigh, matrix, visited_nodes)

## Djikstra
def solve(input_mat):
    source_mat = Matrix(row[:] for row in input_mat)
    first_node = (0, 0)
    visited_nodes = {first_node: source_mat(*first_node)}
    for neighbour in source_mat.neighbours(*first_node):
        visit_node(first_node, neighbour, source_mat, visited_nodes)
    print(visited_nodes[(source_mat.MAX_X, source_mat.MAX_Y)] - source_mat(*first_node))


def heuristic_function(point, mat):
    return abs(mat.MAX_X + 1 - point[0]) + abs(mat.MAX_Y + 1 - point[1])


## A STAR
def reconstruct(trace, node):
    total_path = [node]
    while node in trace:
        node = trace[node]
        total_path.append(node)
    return total_path

def astar(input_mat):
    source_mat = Matrix(row[:] for row in input_mat)
    current = (0,0)
    to_visit = {current: 0}
    visited = {current: 0}
    trace = {}
    while to_visit:
        current = min(((p, k) for (p, k) in to_visit.items()), key=lambda x: x[1])[0]
        if current == (input_mat.MAX_X, input_mat.MAX_Y):
            print("bingo")
            print(sum(input_mat(*p) for p in reconstruct(trace, current)) - input_mat(0, 0))
            return
        del to_visit[current]
        for neighbour in source_mat.neighbours(*current):
            new_score = visited[current] + source_mat(*neighbour)
            if neighbour not in visited or new_score < visited[neighbour]:
                trace[neighbour] = current
                visited[neighbour] = new_score
                to_visit[neighbour] = new_score + heuristic_function(neighbour, source_mat)
                
    
astar(new_mat(mat))
