import re
from dataclasses import dataclass
from typing import Literal


@dataclass
class Range:
    start: int
    end: int


@dataclass
class Cube:
    op: Literal["on", "off"]
    x: Range
    y: Range
    z: Range


def main() -> None:
    cubes: list[Cube] = []
    with open("input.txt") as file:
        for line in file.read().split("\n"):
            op, xrange, yrange, zrange = re.search(
                "(on|off) x=(-?\d+\.\.-?\d+),y=(-?\d+\.\.-?\d+),z=(-?\d+\.\.-?\d+)",
                line,
            ).groups()
            (x1, x2), (y1, y2), (z1, z2) = (
                map(int, coord_range.split(".."))
                for coord_range in (xrange, yrange, zrange)
            )
            cubes.append(Cube(op, Range(x1, x2), Range(y1, y2), Range(z1, z2)))

    grid = [[[0 for _ in range(50)] for _ in range(50)] for _ in range(50)]
    for cube in cubes:
        for x in range(cube.x.start, cube.x.end + 1):
            for y in range(cube.y.start, cube.y.end + 1):
                for z in range(cube.z.start, cube.z.end + 1):
                    if not (0 <= x < 50):
                        continue
                    if not (0 <= y < 50):
                        continue
                    if not (0 <= z < 50):
                        continue
                    grid[x][y][z] = 1 if cube.op == "on" else 0

    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for z in range(len(grid[0][0])):
                count += grid[x][y][z]
    print(count)


if __name__ == "__main__":
    main()
