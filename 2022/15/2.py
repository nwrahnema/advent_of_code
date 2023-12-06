from math import inf

import numpy as np

with open("input.txt") as file:
    grid = np.array(
        [[int(cell) for cell in line] for line in file.read().splitlines()],
        dtype=np.uint8,
    )

row_of_grids = [grid + i for i in range(5)]
grid = np.concatenate(
    [np.concatenate([grid + i for i in range(5)], axis=0) for grid in row_of_grids],
    axis=1,
)
grid = (grid - 1) % 9 + 1

height, width = len(grid), len(grid[0])
min_visited = [[inf for _ in grid[0]] for _ in grid]
min_visited[0][0] = 0

updated = set([(0, 1), (1, 0)])
for _ in range(height * width // 2):
    new_updated = set()
    for i, j in updated:
        adjacent = [
            (i2, j2)
            for i2, j2 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            if 0 <= i2 < height and 0 <= j2 < width
        ]

        min_adjacent = min(min_visited[i2][j2] for i2, j2 in adjacent)
        if min_adjacent + grid[i][j] < min_visited[i][j]:
            min_visited[i][j] = min_adjacent + grid[i][j]
            new_updated.update(adjacent)
    updated = new_updated

print(min_visited[height - 1][width - 1])
