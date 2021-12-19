from itertools import repeat

with open("input.txt") as file:
    oxygen, co2 = repeat(file.readlines(), 2)

    index = 0
    while len(oxygen) > 1:
        bits = [value[index] for value in oxygen]
        most_common = max(["1", "0"], key=bits.count)
        oxygen = [value for value in oxygen if value[index] == most_common]
        index += 1

    index = 0
    while len(co2) > 1:
        bits = [value[index] for value in co2]
        least_common = min(["0", "1"], key=bits.count)
        co2 = [value for value in co2 if value[index] == least_common]
        index += 1

    print(int(oxygen[0], base=2) * int(co2[0], base=2))
