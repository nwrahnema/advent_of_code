from math import prod


with open("input.txt") as file:
    heightmap = [list(line) for line in file.read().splitlines()]

    def fill(i: int, j: int) -> int:
        if not (0 <= i < len(heightmap) and 0 <= j < len(heightmap[i])):
            return 0

        if heightmap[i][j] is None or heightmap[i][j] == "9":
            return 0

        heightmap[i][j] = None
        return (
            sum(
                fill(i2, j2)
                for i2, j2 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            )
            + 1
        )

    basins = [
        fill(i, j) for i in range(len(heightmap)) for j in range(len(heightmap[i]))
    ]
    basins.sort(reverse=True)
    print(prod(basins[:3]))
