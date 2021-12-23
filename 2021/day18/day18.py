from dataclasses import dataclass
from typing import Optional
import pytest

def all_snailfish_pair():
    return [eval(line.strip()) for line in open('input.txt') if line.strip()]


def test_data1():
    return [eval(l) for l in """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".splitlines()]


def test_data2():
    return [eval(l) for l in """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()]


class Explosion(Exception):
    def __init__(self, l, r):
        self.l = l
        self.r = l
        super().__init__()


class BinaryTree:
    pass


@dataclass
class Leaf(BinaryTree):
    value: int
    parent: "Node"

    def as_tuple(self):
        return self.value

    @property
    def breadth(self):
        return 1
    
    @property
    def depth(self):
        return 0
    
    def magnitude(self):
        return self.value

    def leftmost(self):
        return self

    def rightmost(self):
        return self

    def right_neighbour(self):
        if self.parent.left is self:
            return self.parent.right.leftmost()
        
        elif self.parent.right is self and not self.parent.parent:
            return None
            
        return self.parent.right_neighbour()
    
    def left_neighbour(self):
        if self.parent.right is self:
            return self.parent.left.rightmost()
        elif self.parent.left is self and not self.parent.parent:
            return None 
        return self.parent.left_neighbour()


class Node(BinaryTree):
    def __init__(self, left, right, parent=None):
        self.parent = parent
        self.left = Leaf(left, parent=self) if isinstance(left, int) else Node(*left, self)
        self.right = Leaf(right, parent=self) if isinstance(right, int) else Node(*right, self)
        self._exploded = False
        self._splitted = False

    @property
    def exploded(self):
        if self.parent:
            return self.parent.exploded
        else:
            return self._exploded

    @property
    def splitted(self):
        if self.parent:
            return self.parent.splitted
        else:
            return self._splitted

    @property
    def depth(self):
        return 1 + max(self.left.depth, self.right.depth)

    def __repr__(self):
        return f"Node(*{self.as_tuple()})"

    def rightmost(self):
        return self.right.rightmost()

    def leftmost(self):
        return self.left.leftmost()

    def left_neighbour(self):
        if not self.parent:
            return None
        if self.parent.left is self:
            return self.parent.left_neighbour()
        elif self.parent.right is self:
            return self.parent.left.rightmost()
        else:
            return self.parent.left.rightmost()
    
    def right_neighbour(self):
        if not self.parent:
            return None
        if self.parent.right is self:
            return self.parent.right_neighbour()
        elif self.parent.left is self:
            return self.parent.right.leftmost()
        else:
            return self.parent.right.leftmost()
            
    def as_tuple(self):
        return (self.left.as_tuple(), self.right.as_tuple())

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def explode(self, depth=4):
        if self.exploded:
            return

        if depth == 0:
            ## Explosion
            p = self.parent
            while p.parent is not None:
                p = p.parent
            p._exploded = True
            
            assert isinstance(self.left, Leaf)
            assert isinstance(self.right, Leaf)
        
            if neighbour_left := self.left.left_neighbour():
                neighbour_left.value = neighbour_left.value + self.left.value
            if neighbour_right := self.right.right_neighbour():
                neighbour_right.value = neighbour_right.value + self.right.value

            if self.parent.left is self:
                self.parent.left = Leaf(value=0, parent=self.parent)

            elif self.parent.right is self:
                self.parent.right = Leaf(value=0, parent=self.parent)


        if not isinstance(self.left, Leaf):
            self.left.explode(depth=depth - 1)
            
        if not isinstance(self.right, Leaf):
            self.right.explode(depth=depth-1)

        if self.parent is None:
            if self._exploded:
                pass
                # print("after explode:", self.as_tuple())
            self._exploded = False
        return self

    def split(self):
        if self.splitted:
            return
        
        if isinstance(self.left, Leaf) and self.left.value > 9:
            self.left = Node(self.left.value //2, self.left.value // 2 + self.left.value % 2, parent=self)
            ## Split
            p = self.parent
            while p.parent is not None:
                p = p.parent
            p._splitted = True
            return

        elif isinstance(self.left, Node):
            self.left.split()

        if isinstance(self.right, Leaf) and self.right.value > 9 and not self.splitted:
            self.right = Node(self.right.value //2, self.right.value // 2 + self.right.value % 2, parent=self)
            ## Split
            p = self.parent
            while p.parent is not None:
                p = p.parent
            p._splitted = True
            return

        elif isinstance(self.right, Node):
            result = self.right.split()

        if self.parent is None:
            if self._splitted:
                pass
                # print("after split:", self.as_tuple())
            self._splitted = False
        return self

    def must_explode(self):
        assert self.depth <= 5
        return self.depth == 5

    def evolve_all(self, cont=True):
        if not cont:
            return self
        start_value = self.as_tuple()
        while self.must_explode():
            self.explode()
        init_value = self.as_tuple()
        splitted = self.split().as_tuple()
        while init_value != splitted and not self.must_explode():
            init_value = splitted
            splitted = self.split().as_tuple()
        return self.evolve_all(cont=self.must_explode())


def test_right_neighbour_lookup():
    data = Node(*[[[[0, [4, 5]], 6], [3, 8]], 2])
    two = data.right
    zero = data.left.left.left.left
    four = data.left.left.left.right.left
    five = data.left.left.left.right.right
    three = data.left.left.left
    six = data.left.left.right
    three = data.left.right.left
    eight = data.left.right.right
    assert zero.value == 0
    assert two.value == 2
    assert six.value == 6
    assert four.value == 4
    assert five.value == 5
    assert eight.value == 8
    assert three.value == 3
    assert zero.right_neighbour() is four
    assert four.right_neighbour() is five
    assert five.right_neighbour() is six
    assert six.right_neighbour() is three
    assert three.right_neighbour() is eight
    assert eight.right_neighbour() is two
    assert two.right_neighbour() is None

def test_right_neighbour_lookup2():
    data = Node(*[0, [1, [2, [3, 4]]]])
    zero = data.left
    one = data.right.left
    two = data.right.right.left
    three = data.right.right.right.left
    four = data.right.right.right.right
    assert zero.value == 0
    assert one.value == 1
    assert two.value == 2
    assert three.value == 3
    assert four.value == 4
    assert zero.right_neighbour() is one
    assert one.right_neighbour() is two
    assert two.right_neighbour() is three
    assert three.right_neighbour() is four
    assert four.right_neighbour() is None

def test_left_neighbour_lookup():
    data = Node(*[[[[0, [4, 5]], 6], [3, 8]], 2])
    two = data.right
    zero = data.left.left.left.left
    four = data.left.left.left.right.left
    five = data.left.left.left.right.right
    three = data.left.left.left
    six = data.left.left.right
    three = data.left.right.left
    eight = data.left.right.right
    assert zero.value == 0
    assert two.value == 2
    assert six.value == 6
    assert four.value == 4
    assert five.value == 5
    assert eight.value == 8
    assert three.value == 3
    assert two.left_neighbour() is eight
    assert eight.left_neighbour() is three
    assert three.left_neighbour() is six
    assert six.left_neighbour() is five
    assert five.left_neighbour() is four
    assert four.left_neighbour() is zero
    assert zero.left_neighbour() is None


def test_explode_tree():
    data = Node(*[[[[[9,8],1],2],3],4])
    assert data.explode().as_tuple() == Node(*[[[[0,9],2],3],4]).as_tuple()
    assert data.explode().as_tuple() == Node(*[[[[0,9],2],3],4]).as_tuple()
    assert Node(*[7,[6,[5,[4,[3,2]]]]]).explode().as_tuple() == Node(*[7,[6,[5,[7,0]]]]).as_tuple()
    assert Node(*[[6,[5,[4,[3,2]]]],1]).explode().as_tuple() == Node(*[[6,[5,[7,0]]],3]).as_tuple()
    assert Node(*[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]).explode().as_tuple() == Node(*[[3,[2,[8,0]]],[9,[5,[7,0]]]]).as_tuple()


def test_explode_is_single_step():
    assert Node(*[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]).explode().as_tuple() == Node(*[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]).as_tuple()


def test_split():
    assert Node(*[[[[0,7],4],[15,[0,13]]],[1,1]]).split().as_tuple() == Node(*[[[[0,7],4],[[7,8],[0,13]]],[1,1]]).as_tuple()
    assert Node(*[[[[0,7],4],[[7,8],[0,13]]],[1,1]]).split().as_tuple() == Node(*[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]).as_tuple()

def test_buggy_split():
    assert Node(*((((7, 7), (7, 8)), ((9, 5), (8, 0))), (((9, 10), 20), (8, (9, 0))))).split().as_tuple() == Node(*[[[[7,7],[7,8]],[[9,5],[8,0]]],[[[9,[5,5]],20],[8,[9,0]]]]).as_tuple()

def test_magnitude():
    assert Node(*[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).magnitude() == 3488
    assert Node(*[[[[0,7],4],[[7,8],[6,0]]],[8,1]]).magnitude() == 1384
    assert Node(*[[[[5,0],[7,4]],[5,5]],[6,6]]).magnitude() == 1137

def test_evolve1():
    n = Node(*[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]])
    n.evolve_all()
    assert n.as_tuple() == Node(*[[[[0,7],4],[[7,8],[6,0]]],[8,1]]).as_tuple()

def test_evolve2():
    n = Node([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]])
    n.evolve_all()
    assert n.as_tuple() == Node(*[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]).as_tuple()


@pytest.mark.parametrize(
    "vector,output", [
        (([[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]], [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]), [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]),
        (([[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]),[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]),
    ]
)
def test_evolve3(vector, output):
    n = Node(*vector)
    n.evolve_all()
    assert n.as_tuple() == Node(*output).as_tuple()


@pytest.mark.parametrize(
    "vector,output", [
        (([[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]),[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]),
        (([[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],[[2,[2,2]],[8,[8,1]]]),[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]),
        (([[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],[2,9]),[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]),
        (([[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],[1,[[[9,3],9],[[9,0],[0,7]]]]), [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]),
        (([[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],[[[5,[7,4]],7],1]), [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]),
        (([[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],[[[[4,2],2],6],[8,7]]), [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]),
    ]
)
def test_evolve4(vector, output):
    n = Node(*vector)
    n.evolve_all()
    assert n.as_tuple() == Node(*output).as_tuple()

@pytest.mark.parametrize(
 "d", [Node(*[[[[7,7],[7,8]],[[9,5],[8,0]]],[[[9,[5,5]],20],[8,[9,0]]]])]
)
def test_must_explode(d):
    assert d.must_explode()

def test_scenario_1():
    lines = test_data1()
    assert not any(Node(*l).must_explode() for l in lines)
    line1, line2 = lines[:2]
    initial_node = Node(line1, line2)
    initial_node.evolve_all()
    for line in lines[2:]:
        initial_node = Node(initial_node.as_tuple(), line)
        initial_node.evolve_all()
    print(initial_node.magnitude())

def test_scenario_2():
    lines = test_data2()
    assert not any(Node(*l).must_explode() for l in lines)
    line1, line2 = lines[:2]
    initial_node = Node(line1, line2)
    initial_node.evolve_all()
    for line in lines[2:]:
        initial_node = Node(initial_node.as_tuple(), line)
        initial_node.evolve_all()
    assert initial_node.as_tuple() == Node(*[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]).as_tuple()
    assert initial_node.magnitude() == 4140

def test_scenario_3():
    lines = all_snailfish_pair()
    assert not any(Node(*l).must_explode() for l in lines)
    line1, line2 = lines[:2]
    initial_node = Node(line1, line2)
    initial_node.evolve_all()
    for line in lines[2:]:
        initial_node = Node(initial_node.as_tuple(), line)
        initial_node.evolve_all()
    assert initial_node.magnitude() == 4184

def test_scenario_4():
    lines = test_data2()
    all_lines = [
        (l1, l2) for (k, l1) in enumerate(lines) for (j, l2) in enumerate(lines) if k!=j
    ]
    max_magnitude = 0
    for l1, l2 in all_lines:
        node = Node(l1, l2)
        node.evolve_all()
        max_magnitude = max(max_magnitude, node.magnitude())
    assert max_magnitude == 3993

def test_scenario_5():
    lines = all_snailfish_pair()
    all_lines = [
        (l1, l2) for (k, l1) in enumerate(lines) for (j, l2) in enumerate(lines) if k!=j
    ]
    max_magnitude = 0
    for l1, l2 in all_lines:
        node = Node(l1, l2)
        node.evolve_all()
        max_magnitude = max(max_magnitude, node.magnitude())
    assert max_magnitude == 4731
