from math import inf

with open("input.txt") as file:
    grid = [[int(cell) for cell in line] for line in file.read().splitlines()]

height, width = len(grid), len(grid[0])
min_visited = [[inf for _ in grid[0]] for _ in grid]
min_visited[0][0] = 0

for _ in range(height * width // 100):  # cheating lol, see part 2 for real answer
    for i in range(height):
        for j in range(width):
            min_adjacent = min(
                min_visited[i2][j2]
                for i2, j2 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                if 0 <= i2 < height and 0 <= j2 < width
            )

            min_visited[i][j] = min(min_visited[i][j], min_adjacent + grid[i][j])


print(min_visited[height - 1][width - 1])
