import re


def main() -> None:
    with open("input.txt") as file:
        player1, player2 = (
            int(re.search("starting position: (\d)", line).group(1))
            for line in file.read().split("\n")
        )
    die_count = 0
    die = 1
    score1, score2 = 0, 0
    turn = 0

    def take_turn(player: int, score: int) -> tuple[int, int]:
        nonlocal die_count
        nonlocal die
        for _ in range(3):
            player += die
            die += 1
            if die > 100:
                die = 1
            die_count += 1
        score += (player - 1) % 10 + 1
        return player, score

    while score1 < 1000 and score2 < 1000:
        print(f"{die=},{score1=},{score2=},{player1=},{player2=}")
        if turn % 2 == 0:
            player1, score1 = take_turn(player1, score1)
        else:
            player2, score2 = take_turn(player2, score2)
        turn += 1
    print(min(score1, score2) * die_count)


if __name__ == "__main__":
    main()
