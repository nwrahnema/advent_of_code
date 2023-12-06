import itertools

with open("input") as file:
    depths = map(int, file.readlines())
    print(sum(prev < cur for prev, cur in itertools.pairwise(depths)))
