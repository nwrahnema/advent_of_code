from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from math import ceil, floor
from typing import Iterator, Optional


class Side(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass
class TreeNode:
    parent: Optional[Pair]

    @property
    def side(self) -> Optional[Side]:
        if not self.parent:
            return None
        if self.parent.left is self:
            return Side.LEFT
        return Side.RIGHT

    def replace(self, node: Snailfish):
        if self.parent and self.side == Side.LEFT:
            self.parent.left = node
        elif self.parent and self.side == Side.RIGHT:
            self.parent.right = node
        node.parent = self.parent


@dataclass
class Number(TreeNode):
    value: int


@dataclass
class Pair(TreeNode):
    left: Number | Pair
    right: Number | Pair

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def leftmost_child(self) -> Number:
        if isinstance(self.left, Number):
            return self.left
        else:
            return self.left.leftmost_child()

    def rightmost_child(self) -> Number:
        if isinstance(self.right, Number):
            return self.right
        else:
            return self.right.rightmost_child()

    def adjacent_node_left(self) -> Optional[Number]:
        if not self.parent:
            return None

        if self.side == Side.LEFT:
            return self.parent.adjacent_node_left()
        else:
            if isinstance(self.parent.left, Number):
                return self.parent.left
            return self.parent.left.rightmost_child()

    def adjacent_node_right(self) -> Optional[Number]:
        if not self.parent:
            return None

        if self.side == Side.RIGHT:
            return self.parent.adjacent_node_right()
        else:
            if isinstance(self.parent.right, Number):
                return self.parent.right
            return self.parent.right.leftmost_child()


Snailfish = Number | Pair


def parse_snailfish(input: Iterator[str]) -> Snailfish:
    char = next(input)
    if char == "[":

        left = parse_snailfish(input)
        assert next(input) == ","
        right = parse_snailfish(input)
        assert next(input) == "]"

        snailfish = Pair(left=left, right=right, parent=None)
        left.parent = snailfish
        right.parent = snailfish

        return snailfish
    elif char.isnumeric():
        return Number(value=int(char), parent=None)

    raise Exception(
        f"Encountered invalid character: {char}. Expected '[' or an integer."
    )


def try_explode_snailfish(snailfish: Pair, depth=0) -> bool:
    if (
        depth >= 4
        and isinstance(snailfish.left, Number)
        and isinstance(snailfish.right, Number)
    ):
        if node := snailfish.adjacent_node_left():
            node.value += snailfish.left.value
        if node := snailfish.adjacent_node_right():
            node.value += snailfish.right.value

        snailfish.replace(Number(value=0, parent=None))

        return True

    if isinstance(snailfish.left, Pair):
        if try_explode_snailfish(snailfish.left, depth + 1):
            return True
    if isinstance(snailfish.right, Pair):
        if try_explode_snailfish(snailfish.right, depth + 1):
            return True

    return False


def try_split_snailfish(snailfish: Snailfish) -> bool:
    if isinstance(snailfish, Number):
        if snailfish.value >= 10:
            left = Number(value=floor(snailfish.value / 2), parent=None)
            right = Number(value=ceil(snailfish.value / 2), parent=None)
            pair = Pair(left=left, right=right, parent=snailfish.parent)
            left.parent = pair
            right.parent = pair
            snailfish.replace(pair)

            return True
    else:
        if try_split_snailfish(snailfish.left):
            return True
        if try_split_snailfish(snailfish.right):
            return True
    return False


def reduce_snailfish(snailfish: Pair) -> Pair:
    if try_explode_snailfish(snailfish):
        snailfish = reduce_snailfish(snailfish)
    elif try_split_snailfish(snailfish):
        snailfish = reduce_snailfish(snailfish)

    return snailfish


def combine_snailfishes(snailfish1: Snailfish, snailfish2: Snailfish) -> Pair:
    snailfish = Pair(left=snailfish1, right=snailfish2, parent=None)
    snailfish1.parent = snailfish
    snailfish2.parent = snailfish
    return reduce_snailfish(snailfish)


def get_magnitude(snailfish: Snailfish) -> int:
    if isinstance(snailfish, Number):
        return snailfish.value
    else:
        return 3 * get_magnitude(snailfish.left) + 2 * get_magnitude(snailfish.right)


def main():
    with open("input.txt") as file:
        snailfishes = (parse_snailfish(iter(line)) for line in file.read().splitlines())
        result = reduce(combine_snailfishes, snailfishes)
        print(get_magnitude(result))


main()
