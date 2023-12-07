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

total = 0
for card in res:
    winning, mine = card
    intersection = len(winning.intersection(mine))
    total += 0 if intersection == 0 else 2 ** (intersection - 1)

print(total)
