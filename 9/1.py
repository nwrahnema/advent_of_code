with open("input.txt") as file:
    heightmap = file.read().splitlines()
    total = 0
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if all(
                heightmap[i][j] < adjacent
                for adjacent in [
                    heightmap[i - 1][j] if i > 0 else None,
                    heightmap[i][j - 1] if j > 0 else None,
                    heightmap[i + 1][j] if i < len(heightmap) - 1 else None,
                    heightmap[i][j + 1] if j < len(heightmap[i]) - 1 else None,
                ]
                if adjacent is not None
            ):
                total += int(heightmap[i][j]) + 1
    print(total)
