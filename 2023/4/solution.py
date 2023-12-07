import re
from pathlib import Path

with open(Path(__file__).with_name("input.txt")) as f:
    res = [
        [
            set(map(int, group.split()))
            for group in re.search(r"Card\s+\d+: ([\d ]+) \| ([\d ]+)", line).groups()
        ]
        for line in f.read().splitlines()
    ]

counts = [1 for _ in res]
intersections = [len(winning.intersection(mine)) for winning, mine in res]
for i in range(len(intersections)):
    for j in range(i + 1, min(intersections[i] + i + 1, len(intersections))):
        counts[j] += counts[i]

print(sum(counts))
