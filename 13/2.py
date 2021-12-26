from itertools import takewhile

with open("input.txt") as file:
    lines_iter = (line.strip() for line in file)
    dots = set(
        tuple(int(coord) for coord in line.split(","))
        for line in takewhile(bool, lines_iter)
    )
    folds = [line.removeprefix("fold along ").split("=") for line in lines_iter]

    for axis, line in folds:
        line = int(line)
        if axis == "x":
            for x, y in list(dots):
                if x > line:
                    dots.remove((x, y))
                    dots.add(((line * 2 - x), y))
        elif axis == "y":
            for x, y in list(dots):
                if y > line:
                    dots.remove((x, y))
                    dots.add((x, (line * 2 - y)))

    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in dots:
        grid[y][x] = "#"

    for row in grid:
        print(*row)
