from collections import Counter
from functools import cache
from itertools import product
import re

THREE_ROLL_DISTRIBUTION = Counter(sum(rolls) for rolls in product((1, 2, 3), repeat=3))
WIN_SCORE = 21


@cache
def play(score: int, other_score: int, pos: int, other_pos: int):
    print(score, other_score, pos, other_pos)
    if score >= WIN_SCORE:
        return 1, 0
    if other_score >= WIN_SCORE:
        return 0, 1

    total_universes, total_other_universes = 0, 0
    for distance, count in THREE_ROLL_DISTRIBUTION.items():
        next_pos = (pos + distance) % 10
        next_score = score + (next_pos + 1)
        other_universes, universes = play(other_score, next_score, other_pos, next_pos)
        total_universes += universes * count
        total_other_universes += other_universes * count
    return total_universes, total_other_universes


def main() -> None:
    with open("input.txt") as file:
        player1, player2 = (
            int(re.search("starting position: (\d)", line).group(1)) - 1
            for line in file.read().split("\n")
        )
    print(play(0, 0, player1, player2))


if __name__ == "__main__":
    main()
