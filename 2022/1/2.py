from itertools import pairwise
from more_itertools import windowed

with open("input") as file:
    depths = map(int, file.readlines())
    windows = map(sum, windowed(depths, 3))
    print(sum(prev < cur for prev, cur in pairwise(windows)))
