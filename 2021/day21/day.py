import itertools

from collections import Counter


def deterministic_game(p1, p2, dice, dice_limit=1000):
    new_p1_score = new_p2_score = 0
    while True:
        new_p1_score = p1.turn(dice)
        if new_p1_score >= dice_limit:
            print("p1 wins; answer1:", new_p2_score * dice.nb_rolls)
            break
        new_p2_score = p2.turn(dice)
        if new_p2_score >= dice_limit:
            print("p2 wins; answer 1:", new_p1_score * dice.nb_rolls)
            break


def dirac_game(p1, p2, dice_limit=21, p1_turn=True, depth=0):
    player = p1 if p1_turn else p2
    final_number_of_wins = 0
    for score, coef in {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}.items():
        new_player = Player(player.position, player.score)
        new_player.update_score(score)
        if p1_turn and new_player.score >= dice_limit:
            final_number_of_wins += coef
        elif not p1_turn and new_player.score >= dice_limit:
            final_number_of_wins += 0
        else:
            args = (new_player, p2) if p1_turn else (p1, new_player)
            kwargs = {'p1_turn': not p1_turn, 'depth': depth + 1, 'dice_limit': dice_limit}
            final_number_of_wins += (coef * dirac_game(*args, **kwargs))
    return final_number_of_wins


def dirac_tree(start=(), depth=3):
    if depth == 0:
        yield start
    else:
        for d in (1, 2, 3):
            yield from dirac_tree(start + (d, ), depth=depth - 1)


def dirac_probabilities():
    return Counter(sum(path) for path in dirac_tree())


class Player:
    def __init__(self, start_at, score=0):
        self.position = start_at
        self.score = score

    def roll_dice(self, dice):
        r1 = dice.roll()
        r2 = dice.roll()
        r3 = dice.roll()
        return r1 + r2 + r3

    def turn(self, dice):
        r = self.roll_dice(dice)
        return self.update_score(r)

    def update_score(self, dice_result: int):
        new_position = (self.position + dice_result)
        if new_position % 10 == 0:
            new_position = 10
        else:
            new_position = new_position % 10
        self.position = new_position
        self.score += new_position
        return self.score


class DiracPlayer(Player):
    pass


class DeterministicDice:
    def __init__(self):
        self.nb_rolls = 0
        self.generator = self.roll_generator()

    def roll(self):
        return next(self.generator)

    def roll_generator(self):
        for val in itertools.cycle(range(1, 101)):
            self.nb_rolls += 1
            yield val


p1 = Player(4)
p2 = Player(5)

deterministic_game(p1, p2, DeterministicDice())

p1 = DiracPlayer(4)
p2 = DiracPlayer(5)

print(dirac_game(p1, p2))
