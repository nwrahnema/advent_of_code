from dataclasses import dataclass
from itertools import chain, repeat, zip_longest


@dataclass
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
        start, end = map(Position.of_string, string.split("->"))
        return Line(start, end)


with open("input.txt") as file:
    lines = [Line.of_string(line) for line in file.readlines()]

    max_y = max(chain.from_iterable((line.start.y, line.end.y) for line in lines))
    max_x = max(chain.from_iterable((line.start.x, line.end.x) for line in lines))

    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for line in lines:
        num_points = max(
            abs(line.end.y - line.start.y), (abs(line.end.x - line.start.x))
        )
        x_move = (line.end.x - line.start.x) // num_points
        y_move = (line.end.y - line.start.y) // num_points
        for i in range(num_points + 1):
            grid[line.start.y + (y_move * i)][line.start.x + (x_move * i)] += 1

    print(sum(count > 1 for count in chain(*grid)))
