from collections import defaultdict
from dataclasses import dataclass
from itertools import chain, product
from math import copysign
import re
from typing import Iterable


@dataclass
class TargetArea:
    x1: int
    x2: int
    y1: int
    y2: int


def get_x_positions(velocity: int) -> Iterable[int]:
    pos = 0
    while True:
        pos += velocity
        velocity += copysign(1, velocity) * -1 if velocity else 0
        yield pos


def get_y_positions(velocity: int) -> Iterable[int]:
    pos = 0
    while True:
        pos += velocity
        velocity -= 1
        yield pos


def get_x_steps(target_area: TargetArea, max_steps: int) -> dict[int, list[int]]:
    x_steps = defaultdict(list)
    for x_velocity in range(target_area.x2 + 1):
        for i, x_position in enumerate(get_x_positions(x_velocity)):
            if i > max_steps:
                break
            if target_area.x1 <= x_position <= target_area.x2:
                x_steps[i].append(x_velocity)
    return x_steps


def get_y_steps(target_area: TargetArea) -> dict[int, list[int]]:
    y_steps = defaultdict(list)
    for y_velocity in range(
        target_area.y1, max(target_area.y2, abs(target_area.y1)) + 1
    ):
        for i, y_position in enumerate(get_y_positions(y_velocity)):
            if target_area.y1 <= y_position <= target_area.y2:
                y_steps[i].append(y_velocity)
            elif y_position < target_area.y1:
                break
    return y_steps


def main():
    with open("input.txt") as file:
        number_regex = r"-?\d+"
        x1, x2, y1, y2 = map(
            int,
            re.search(
                fr"target area: x=({number_regex})\.\.({number_regex}), y=({number_regex})\.\.({number_regex})",
                file.read(),
            ).groups(),
        )

    target_area = TargetArea(x1, x2, y1, y2)

    y_steps = get_y_steps(target_area)
    x_steps = get_x_steps(target_area, max(y_steps))

    velocities = set(
        chain.from_iterable(product(x_steps[key], y_steps[key]) for key in y_steps)
    )
    print(len(velocities))


main()
