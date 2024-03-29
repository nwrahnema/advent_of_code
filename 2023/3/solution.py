from pathlib import Path

with open(Path(__file__).with_name("input.txt")) as f:
    grid = f.read().splitlines()

star_counts = [[[] for _ in grid[0]] for _ in grid]

i = 0
while i < len(grid):
    j = 0
    while j < len(grid[i]):
        if grid[i][j].isdigit():
            number = []
            found = set()
            while j < len(grid[i]) and grid[i][j].isdigit():
                number += grid[i][j]
                for x in [
                    coord for coord in [i - 1, i, i + 1] if 0 <= coord < len(grid)
                ]:
                    for y in [
                        coord
                        for coord in [j - 1, j, j + 1]
                        if 0 <= coord < len(grid[x])
                    ]:
                        if grid[x][y] == "*":
                            found.add((x, y))
                j += 1
            for x, y in found:
                star_counts[x][y].append(int("".join(number)))
        j += 1
    i += 1

print(sum(lst[0] * lst[1] for row in star_counts for lst in row if len(lst) == 2))
