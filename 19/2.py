from dataclasses import dataclass
from functools import cache, cached_property
from itertools import combinations, permutations, product
import numpy as np
from typing import NewType, Optional

PositionDelta = NewType("PositionDelta", tuple[int, ...])


@cache
def get_rotation_matrices(d: int) -> list[np.ndarray]:
    result = []
    for axes in permutations(range(d)):
        for inversions in product([-1, 1], repeat=d):
            rotation_matrix = np.zeros((d, d))
            for i, (axis, inversion) in enumerate(zip(axes, inversions)):
                rotation_matrix[i, axis] = inversion
            if np.linalg.det(rotation_matrix) == 1:
                result.append(rotation_matrix)
    return result


@dataclass(frozen=True)
class Position:
    coords: tuple[int, ...]

    def add_delta(self, delta: PositionDelta) -> PositionDelta:
        return Position(tuple(x + y for x, y in zip(self.coords, delta)))

    def distance(self, other: "Position") -> int:
        return sum(abs(x - y) for x, y in zip(self.coords, other.coords))

    def __sub__(self, other: "Position") -> PositionDelta:
        return PositionDelta(tuple(x - y for x, y in zip(self.coords, other.coords)))


@dataclass
class BeaconGroup:
    scanners: list[Position]
    beacons: list[Position]

    @cached_property
    def rotations(self) -> list["BeaconGroup"]:
        rotation_matrices = get_rotation_matrices(len(self.beacons[0].coords))
        return [
            BeaconGroup(
                scanners=[
                    Position(tuple(map(int, np.matmul(matrix, scanner.coords))))
                    for scanner in self.scanners
                ],
                beacons=[
                    Position(tuple(map(int, np.matmul(matrix, beacon.coords))))
                    for beacon in self.beacons
                ],
            )
            for matrix in rotation_matrices
        ]

    @cached_property
    def deltas(self) -> list[tuple[Position, set[PositionDelta]]]:
        return [
            (
                base,
                set(beacon - base for beacon in self.beacons),
            )
            for base in self.beacons
        ]


def try_merge_beacon_groups(
    group1: BeaconGroup, group2: BeaconGroup, threshold: int = 3
) -> Optional[BeaconGroup]:
    for base1, deltas1 in group1.deltas:
        for base2, deltas2 in group2.deltas:
            if len(deltas1.intersection(deltas2)) >= threshold:
                adjust = base1 - base2
                return BeaconGroup(
                    scanners=(
                        group1.scanners
                        + [scanner.add_delta(adjust) for scanner in group2.scanners]
                    ),
                    beacons=list(
                        set(
                            group1.beacons
                            + [beacon.add_delta(adjust) for beacon in group2.beacons]
                        )
                    ),
                )
    return None


def main() -> None:
    with open("input.txt") as file:
        scanner_inputs = [
            scanner_input.splitlines() for scanner_input in file.read().split("\n\n")
        ]
        beacon_groups: list[BeaconGroup] = [
            BeaconGroup(
                scanners=[Position((0,) * len(scanner_input[1].split(",")))],
                beacons=[
                    Position(tuple(int(coord) for coord in beacon.split(",")))
                    for beacon in scanner_input[1:]
                ],
            )
            for scanner_input in scanner_inputs
        ]

    i, j = 0, 1
    while len(beacon_groups) > 1:
        group1 = beacon_groups[i]
        group2 = beacon_groups[j]
        for rotation in group2.rotations:
            if scanner := try_merge_beacon_groups(group1, rotation):
                beacon_groups.pop(j)
                beacon_groups.pop(i)
                beacon_groups.append(scanner)
                j = i
                break

        j += 1
        if j >= len(beacon_groups):
            i += 1
            j = i + 1

    (beacon_group,) = beacon_groups
    print(
        max(
            scanner1.distance(scanner2)
            for scanner1, scanner2 in combinations(beacon_group.scanners, 2)
        )
    )


if __name__ == "__main__":
    main()
