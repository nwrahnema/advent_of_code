import re
from enum import Enum
from pathlib import Path


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def parse_color_count(string: str, color: Color) -> int:
    res = re.search(rf"(\d+) {color.value}", string)
    if res is not None:
        return int(res.group(1))
    return 0


with open(Path(__file__).with_name("input.txt")) as f:
    games: dict[int, list[dict[Color, int]]] = {}
    for line in f.read().splitlines():
        game_id, game = re.search(r"Game (\d+): (.*)", line).groups()
        games[int(game_id)] = [
            {color: parse_color_count(reveal, color) for color in Color}
            for reveal in game.split("; ")
        ]

totals = {Color.RED: 12, Color.GREEN: 13, Color.BLUE: 14}

result = 0
for game_id, game in games.items():
    if not any(
        round[color] > total for round in game for color, total in totals.items()
    ):
        result += game_id

print(result)
