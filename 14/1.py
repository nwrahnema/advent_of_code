from itertools import zip_longest
from typing import Counter

with open("input.txt") as file:
    (polymer, insertion_rules) = file.read().split("\n\n")
    insertion_rules = {
        tuple(pair.strip()): result.strip()
        for pair, result in [rule.split("->") for rule in insertion_rules.splitlines()]
    }

for _ in range(10):
    insertions = [insertion_rules[pair] for pair in zip(polymer[:-1], polymer[1:])]
    polymer = [
        element
        for interleaved in zip_longest(polymer, insertions)
        for element in interleaved
        if element
    ]

most_common = [count for _, count in Counter(polymer).most_common()]
print(most_common[0] - most_common[-1])
