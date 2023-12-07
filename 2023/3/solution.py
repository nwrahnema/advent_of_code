from pathlib import Path

with open(Path(__file__).with_name("input.txt")) as f:
    grid = f.read().splitlines()

total = 0

i = 0
while i < len(grid):
    j = 0
    while j < len(grid[i]):
        if grid[i][j].isdigit():
            number = []
            found = False
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
                        if not grid[x][y].isalnum() and grid[x][y] != ".":
                            found = True
                j += 1
            if found:
                total += int("".join(number))
        j += 1
    i += 1

print(total)
