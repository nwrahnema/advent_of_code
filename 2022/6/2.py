from collections import Counter

with open("input.txt") as file:
    fish = Counter(map(int, file.readline().split(",")))
    for _ in range(256):
        new_fish = Counter()
        for days_left, count in fish.items():
            new_fish.update(
                {6: count, 8: count} if days_left == 0 else {days_left - 1: count}
            )
        fish = new_fish

    print(sum(fish.values()))
