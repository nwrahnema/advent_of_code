import re
from enum import Enum
from math import prod
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


result = 0
for game in games.values():
    maxes = {color: 0 for color in Color}
    for round in game:
        for color, count in round.items():
            maxes[color] = max(maxes[color], count)
    result += prod(maxes.values())

print(result)
