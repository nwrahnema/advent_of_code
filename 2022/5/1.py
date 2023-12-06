from dataclasses import dataclass
from itertools import chain


@dataclass(order=True)
class Position:
    x: int
    y: int

    def of_string(string: str) -> "Position":
        x, y = string.split(",")
        return Position(int(x), int(y))


@dataclass
class Line:
    start: Position
    end: Position

    def of_string(string: str) -> "Line":
        positions = map(Position.of_string, string.split("->"))
        start, end = sorted(positions)
        return Line(start, end)


with open("input.txt") as file:
    lines = [Line.of_string(line) for line in file.readlines()]
    lines = [
        line
        for line in lines
        if line.start.x == line.end.x or line.start.y == line.end.y
    ]

    max_y = max(chain.from_iterable((line.start.y, line.end.y) for line in lines))
    max_x = max(chain.from_iterable((line.start.x, line.end.x) for line in lines))

    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for line in lines:
        for y in range(line.start.y, line.end.y + 1):
            for x in range(line.start.x, line.end.x + 1):
                grid[y][x] += 1

    print(sum(count > 1 for count in chain(*grid)))
