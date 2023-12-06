from itertools import takewhile

with open("input.txt") as file:
    lines_iter = (line.strip() for line in file)
    dots = set(
        tuple(int(coord) for coord in line.split(","))
        for line in takewhile(bool, lines_iter)
    )
    folds = [line.removeprefix("fold along ").split("=") for line in lines_iter]

    axis, line = folds[0]
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

    print(len(dots))
