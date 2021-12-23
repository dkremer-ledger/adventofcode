from typing import TypeAlias, List
Board: TypeAlias = List


def read_board(f) -> Board:
    output = []
    for y in range(5):
        data = f.readline()
        output.append(list(map(int, data.strip().split())))
    return output


def board_into_coordinates(board: Board):
    result = {}
    for y, row in enumerate(board):
        for x, number in enumerate(row):
            result[number] = (y, x)
            assert board[y][x] == number
    return result


def empty_board() -> Board:
    return [[None for _ in range(5)] for _ in range(5)]


with open('day4.txt') as f:
    bingo_numbers = list(map(int, f.readline().strip().split(',')))
    all_boards = []
    empty = f.readline()
    while empty:
        all_boards.append(read_board(f))
        empty = f.readline()
    mapped_boards = [board_into_coordinates(b) for b in all_boards]


win_at = []
counter = 0
for board_map, board in zip(mapped_boards, all_boards):
    for counter, number in enumerate(bingo_numbers):
        try:
            y, x = board_map[number]
        except KeyError:
            continue
        board[y][x] = None
        if any(all(n is None for n in row) for row in board):
            win_at.append(counter)
            break
        if any(all(n is None for n in row) for row in zip(*board)):
            win_at.append(counter)
            break
    else:
        win_at.append(None)
print("### PART 1 ###")
winning_board_index = win_at.index(min(win_at))
print("winning board index: ", winning_board_index)
print("Unmarked Numbers sum: ", sum(sum(n for n in row if n is not None) for row in all_boards[winning_board_index]))
print("Last Winning Number: ", bingo_numbers[min(win_at)])
print("### PART 2 ###")
winning_board_index = win_at.index(max(win_at))
print("losing board index: ", winning_board_index)
print("Unmarked Numbers sum: ", sum(sum(n for n in row if n is not None) for row in all_boards[winning_board_index]))
print("Last Losing Number: ", bingo_numbers[max(win_at)])

