from typing import Counter

with open("input.txt") as file:
    (polymer, insertion_rules) = file.read().split("\n\n")
    polymer_pairs = Counter(zip(polymer[:-1], polymer[1:]))
    insertion_rules = {
        tuple(pair.strip()): result.strip()
        for pair, result in [rule.split("->") for rule in insertion_rules.splitlines()]
    }

polymer_count = Counter(polymer)
for _ in range(40):
    polymer_pairs_new = Counter()

    for pair, count in polymer_pairs.items():
        left, right = pair
        insertion = insertion_rules[pair]

        polymer_pairs_new[(left, insertion)] += count
        polymer_pairs_new[(insertion, right)] += count
        polymer_count[insertion] += count

    polymer_pairs = polymer_pairs_new

most_common = [count for _, count in polymer_count.most_common()]
print(most_common[0] - most_common[-1])
