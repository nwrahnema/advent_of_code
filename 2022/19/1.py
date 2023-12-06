from dataclasses import dataclass
from functools import cache, cached_property
from itertools import permutations, product
import numpy as np
from typing import NewType, Optional

Beacon = NewType("Beacon", tuple[int, ...])
ScannerDeltas = NewType("ScannerDeltas", set[tuple[int, ...]])


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


@dataclass
class Scanner:
    beacons: list[Beacon]

    @cached_property
    def rotations(self) -> list["Scanner"]:
        rotation_matrices = get_rotation_matrices(len(self.beacons[0]))
        return [
            Scanner(
                beacons=[
                    tuple(map(int, np.matmul(matrix, beacon)))
                    for beacon in self.beacons
                ],
            )
            for matrix in rotation_matrices
        ]

    @cached_property
    def deltas(self) -> list[ScannerDeltas]:
        return [
            ScannerDeltas(
                set(
                    tuple(y - x for x, y in zip(base, beacon))
                    for beacon in self.beacons
                )
            )
            for base in self.beacons
        ]


def try_merge_scanners(
    scanner1: Scanner, scanner2: Scanner, threshold: int = 12
) -> Optional[Scanner]:
    for deltas1 in scanner1.deltas:
        for deltas2 in scanner2.deltas:
            if len(deltas1.intersection(deltas2)) >= threshold:
                return Scanner(beacons=list(deltas1.union(deltas2)))
    return None


def main() -> None:
    with open("test.txt") as file:
        scanner_inputs = [
            scanner_input.splitlines() for scanner_input in file.read().split("\n\n")
        ]
        scanners: list[Scanner] = [
            Scanner(
                beacons=[
                    Beacon(tuple(int(coord) for coord in beacon.split(",")))
                    for beacon in scanner_input[1:]
                ],
            )
            for scanner_input in scanner_inputs
        ]

    i, j = 0, 1
    while len(scanners) > 1:
        scanner1 = scanners[i]
        scanner2 = scanners[j]
        for rotation in scanner1.rotations:
            if scanner := try_merge_scanners(rotation, scanner2):
                scanners.pop(j)
                scanners.pop(i)
                scanners.append(scanner)
                j = i
                break

        j += 1
        if j >= len(scanners):
            i += 1
            j = i + 1

    print(len(scanners[0].beacons))


if __name__ == "__main__":
    main()
