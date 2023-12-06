with open("input.txt") as file:
    octopuses = [list(map(int, line)) for line in file.read().splitlines()]
    total_flashes = 0

    for _ in range(100):
        will_flash = []

        for i in range(len(octopuses)):
            for j in range(len(octopuses[i])):
                octopuses[i][j] += 1
                if octopuses[i][j] == 10:
                    will_flash.append((i, j))

        while will_flash:
            i, j = will_flash.pop()

            for i2, j2 in [
                (i + di, j + dj)
                for di in (-1, 0, 1)
                for dj in (-1, 0, 1)
                if di != 0 or dj != 0
            ]:
                if not (0 <= i2 < len(octopuses) and 0 <= j2 < len(octopuses[i2])):
                    continue

                octopuses[i2][j2] += 1
                if octopuses[i2][j2] == 10:
                    will_flash.append((i2, j2))

            total_flashes += 1

        for i in range(len(octopuses)):
            for j in range(len(octopuses[i])):
                if octopuses[i][j] > 9:
                    octopuses[i][j] = 0

    print(total_flashes)
