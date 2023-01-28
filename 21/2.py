from collections import Counter, defaultdict
from functools import reduce
from itertools import product
import re

THREE_ROLL_DISTRIBUTION = Counter(sum(rolls) for rolls in product((1, 2, 3), repeat=3))
WIN_SCORE = 21
MAX_SCORE = WIN_SCORE + 10
MAX_TURNS = WIN_SCORE


def get_wins_by_turn(starting_pos: int):
    dp = [
        [[0 for _ in range(10)] for _ in range(MAX_SCORE + 1)]
        for _ in range(MAX_TURNS + 1)
    ]
    dp[0][0][starting_pos] = 1

    for turn in range(1, MAX_TURNS + 1):
        for score in range(1, MAX_SCORE + 1):
            for pos in range(10):
                prev_score = score - (pos + 1)
                if 0 <= prev_score < WIN_SCORE:
                    for distance, count in THREE_ROLL_DISTRIBUTION.items():
                        dp[turn][score][pos] += (
                            dp[turn - 1][prev_score][(pos - distance) % 10] * count
                        )

    wins_by_turn = defaultdict(int)
    for turn in range(1, MAX_TURNS + 1):
        for score in range(WIN_SCORE, MAX_SCORE + 1):
            for pos in range(10):
                wins_by_turn[turn] += dp[turn][score][pos]
    return wins_by_turn


def main() -> None:
    with open("test.txt") as file:
        player1, player2 = (
            int(re.search("starting position: (\d)", line).group(1)) - 1
            for line in file.read().split("\n")
        )
    possibilities_by_turn = reduce(
        lambda acc, val: {
            **acc,
            val: acc[val - 1] * sum(THREE_ROLL_DISTRIBUTION.values()),
        },
        range(1, MAX_TURNS * 2 + 1),
        {0: 1},
    )
    print(possibilities_by_turn)

    wins_by_turn1 = get_wins_by_turn(player1)
    wins_by_turn2 = get_wins_by_turn(player2)

    print(wins_by_turn1)
    print(wins_by_turn2)

    player1_wins = defaultdict(int)
    player2_wins = defaultdict(int)
    for turn in range(1, MAX_TURNS + 1):
        player1_wins[turn] = (
            player1_wins[turn - 1]
            + (possibilities_by_turn[(turn - 1) * 2] - player2_wins[turn - 1])
            * wins_by_turn1[turn]
        )
        player2_wins[turn] = (
            player2_wins[turn - 1]
            + (possibilities_by_turn[turn * 2 - 1] - player1_wins[turn])
            * wins_by_turn2[turn]
        )

    print(player1_wins)
    print(player2_wins)


if __name__ == "__main__":
    main()
