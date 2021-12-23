data = [l.strip() for l in """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()]

data = [l.strip() for l in open('input.txt')]
opening = {'[', '(', '{', '<'}
closing = {']', ')', '}', '>'}
matching = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>',
}
matching_reversed = {c: o for o, c in matching.items()}
scoring = {']': 57, ')':3, '}':1197, '>':25137}
auto_scoring = {')': 1, ']': 2, '}': 3, '>': 4}
def is_valid(line, store=None):
    queue = []
    if store is None:
        store = []
    for char in line:
        if char in opening:
            queue.append(char)
            continue
        try:
            o = queue.pop()
        except IndexError:
            store.append(char)
            break
        if matching[o] != char:
            store.append(char)
            break
    else:
        return True


def missing_chars(line, store=None):
    queue = []
    if store is None:
        store = []
    for char in line:
        if char in opening:
            queue.append(char)
        else:
            o = queue.pop()
    missing_chars = []
    while queue:
        c = queue.pop()
        missing_chars.append(matching[c])
    return missing_chars

def score_missing_chars(missing):
    initial_score = 0
    for char in missing:
        s = auto_scoring[char]
        initial_score *= 5
        initial_score += s
    return initial_score

store = []
new_data = [line for line in data if is_valid(line, store)]
print(sum(scoring[c] for c in store))
autocomplete_scores = [score_missing_chars(missing_chars(line)) for line in new_data]
print(sorted(autocomplete_scores)[len(autocomplete_scores)//2])
