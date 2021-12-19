with open("input.txt") as file:
    crabs = list(map(int, file.readline().split(",")))
    print(
        min(
            sum(abs(crab - position) for crab in crabs)
            for position in range(min(crabs), max(crabs) + 1)
        )
    )
