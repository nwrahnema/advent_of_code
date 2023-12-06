from collections import defaultdict
from typing import DefaultDict

with open("input.txt") as file:
    entries = [
        [entry_part.strip().split(" ") for entry_part in line.split("|")]
        for line in file.readlines()
    ]

    total = 0
    for patterns, output in entries:
        patterns_by_length: DefaultDict[int, list[set[str]]] = defaultdict(list)
        for pattern in patterns:
            patterns_by_length[len(pattern)].append(set(pattern))

        decoded: dict[str, set[str]] = {}
        for digit, unique_length in (("1", 2), ("4", 4), ("7", 3), ("8", 7)):
            (pattern,) = patterns_by_length[unique_length]
            decoded[digit] = pattern

        (decoded["2"],) = [
            pattern
            for pattern in patterns_by_length[5]
            if len(pattern.intersection(decoded["4"])) == 2
        ]

        (decoded["3"],) = [
            pattern
            for pattern in patterns_by_length[5]
            if len(pattern.intersection(decoded["1"])) == 2
        ]

        (decoded["5"],) = [
            pattern
            for pattern in patterns_by_length[5]
            if pattern not in [decoded["2"], decoded["3"]]
        ]

        (decoded["6"],) = [
            pattern
            for pattern in patterns_by_length[6]
            if len(pattern.intersection(decoded["1"])) == 1
        ]

        (decoded["9"],) = [
            pattern
            for pattern in patterns_by_length[6]
            if len(pattern.intersection(decoded["4"])) == 4
        ]

        (decoded["0"],) = [
            pattern
            for pattern in patterns_by_length[6]
            if pattern not in [decoded["6"], decoded["9"]]
        ]

        reverse_decoded = {
            "".join(sorted(pattern)): digit for digit, pattern in decoded.items()
        }

        total += int(
            "".join(reverse_decoded["".join(sorted(pattern))] for pattern in output)
        )
    print(total)
