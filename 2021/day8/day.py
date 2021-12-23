from collections import Counter

data = []

def yy():
    return open('input.txt')
def xx():
    return filter(None, """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".splitlines())

for line in yy():
    all_digits, four_display = line.split(' | ')
    all_digits = sorted([''.join(sorted(x)) for x in all_digits.split()], key=lambda x: (len(x), x))
    four_display = [''.join(sorted(d)) for d in four_display.split()]
    data.append((all_digits, four_display))

SEGMENTS = {
  0: 6,
  1: 2,
  2: 5,
  3: 5,
  4: 4,
  5: 5,
  6: 6,
  7: 3,
  8: 7,
  9: 6,
}

SIZE = {
  2: (1, ),
  3: (7, ),
  4: (4, ),
  5: (2, 3, 5, ),
  6: (0, 6, 9),
  7: (8, )
}

UNIQUE_SIZE = {
  2: 1,
  3: 7,
  4: 4,
  7: 8,
}

NORMAL_OUTPUT = {
    'cf': 1,
    "acf": 7,
    'bcdf': 4,
    'acdeg': 2,
    'abdfg': 5,
    'acdfg': 3,
    'abcefg': 0,
    'abdefg': 6,
    'abcdfg': 9,
    'abcdefg': 8,
}
ALL_SEGMENTS = 'abcdefg'

d = Counter()
for _, output_value in data:
    for digit in output_value:
        d[SIZE[len(digit)]] += 1
print(d[(1, )] + d[(7, )] + d[(4, )] + d[(8, )])


def make_code(digits):
    output_map = {}

    mapped_digits = {
        UNIQUE_SIZE[len(d)]: d
        for d in digits
        if len(d) in UNIQUE_SIZE
    }

    counter = Counter()

    for d in digits:
        counter.update(d)
    
    for key, value in counter.items():
        if value == 4:
            output_map[key] = 'e'
        if value == 6:
            output_map[key] = 'b'
        if value == 9:
            output_map[key] = 'f'

    one = mapped_digits[1]
    four = mapped_digits[4]
    seven = mapped_digits[7]
    eight = mapped_digits[8]
    
    cee = ''.join(x for x in one if output_map.get(x) != 'f')
    assert len(cee) == 1
    output_map[cee] = 'c'
    
    dee = ''.join(
        l for l in four if output_map.get(l) not in (
            'f',
            'b',
            'c'
        )
    )
    assert len(dee) == 1
    output_map[dee] = 'd'
    
    aaa = ''.join(
        l for l in seven
        if output_map.get(l) not in ('c', 'f')
    )
    assert len(aaa) == 1
    output_map[aaa] = 'a'
    
    last_one = (set(ALL_SEGMENTS) - set(output_map))
    last_target = (set(ALL_SEGMENTS) - set(output_map.values()))
    assert len(last_one) == len(last_target) == 1
    output_map[last_one.pop()] = last_target.pop()
    
    code = {}
    for input_d in digits:
        code[input_d] = ''.join(sorted(output_map[x] for x in input_d))
    assert set(code.values()) == set(NORMAL_OUTPUT.keys())
    
    return code
        

r = 0
for digits, output_value in data:
    code = make_code(digits)
    integer_digits = ''.join(str(NORMAL_OUTPUT[code[d]]) for d in output_value)
    print(integer_digits.lstrip('0'))
    r += int(integer_digits.lstrip('0'))

print(r)
