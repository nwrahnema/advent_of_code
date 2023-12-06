def get_fuel_cost(distance: int) -> int:
    return (distance * (distance + 1)) // 2


with open("input.txt") as file:
    crabs = list(map(int, file.readline().split(",")))
    print(
        min(
            sum(get_fuel_cost(abs(crab - position)) for crab in crabs)
            for position in range(min(crabs), max(crabs) + 1)
        )
    )
