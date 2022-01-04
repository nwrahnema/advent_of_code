from dataclasses import dataclass
from itertools import islice
from typing import Iterator
from math import prod


class StringReader:
    count: int = 0

    def __init__(self, string_iter: Iterator[str]):
        self.string_iter = string_iter

    def take(self, n: int) -> str:
        self.count += n
        return "".join(islice(self.string_iter, n))


@dataclass
class Result:
    value: int
    bits_read: int


def decode(packet: Iterator[str]) -> Result:
    string_reader = StringReader(packet)

    string_reader.take(3)  # version number
    type_id = int(string_reader.take(3), 2)
    if type_id == 4:
        literal_value = ""

        is_last = False
        while not is_last:
            is_last = string_reader.take(1) == "0"
            literal_value += string_reader.take(4)

        return Result(int(literal_value, 2), string_reader.count)
    else:
        length_type_id = int(string_reader.take(1), 2)
        subpacket_bits_read = 0
        subpacket_values = []

        if length_type_id == 0:
            length = int(string_reader.take(15), 2)

            while subpacket_bits_read < length:
                result = decode(packet)
                subpacket_values.append(result.value)
                subpacket_bits_read += result.bits_read
        elif length_type_id == 1:
            num_subpackets = int(string_reader.take(11), 2)

            for _ in range(num_subpackets):
                result = decode(packet)
                subpacket_values.append(result.value)
                subpacket_bits_read += result.bits_read
        else:
            raise Exception(f"Invalid length type ID: {length_type_id}")

        value = None
        match type_id:
            case 0:
                value = sum(subpacket_values)
            case 1:
                value = prod(subpacket_values)
            case 2:
                value = min(subpacket_values)
            case 3:
                value = max(subpacket_values)
            case 5:
                first, second = subpacket_values
                value = int(first > second)
            case 6:
                first, second = subpacket_values
                value = int(first < second)
            case 7:
                first, second = subpacket_values
                value = int(first == second)
            case _:
                raise Exception(f"Invalid type ID: {type_id}")

        return Result(value, string_reader.count + subpacket_bits_read)


with open("input.txt") as file:
    (packet,) = file.read().splitlines()

# convert hex to binary string without losing leading zeros
packet = f"{int('1' + packet, 16):b}"[1:]

result = decode(iter(packet))

print(result.value)
