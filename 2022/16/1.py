from dataclasses import dataclass
from itertools import islice
from typing import Iterator


class StringReader:
    count: int = 0

    def __init__(self, string_iter: Iterator[str]):
        self.string_iter = string_iter

    def take(self, n: int) -> str:
        self.count += n
        return "".join(islice(self.string_iter, n))


@dataclass
class Result:
    version: int
    bits_read: int


def decode(packet: Iterator[str]) -> Result:
    string_reader = StringReader(packet)

    version_total = int(string_reader.take(3), 2)
    type_id = int(string_reader.take(3), 2)
    if type_id == 4:
        literal_value = ""

        is_last = False
        while not is_last:
            is_last = string_reader.take(1) == "0"
            literal_value += string_reader.take(4)

        return Result(version_total, string_reader.count)
    else:
        length_type_id = int(string_reader.take(1), 2)
        subpacket_bits_read = 0

        if length_type_id == 0:
            length = int(string_reader.take(15), 2)

            while subpacket_bits_read < length:
                result = decode(packet)
                version_total += result.version
                subpacket_bits_read += result.bits_read
        elif length_type_id == 1:
            num_subpackets = int(string_reader.take(11), 2)

            for _ in range(num_subpackets):
                result = decode(packet)
                version_total += result.version
                subpacket_bits_read += result.bits_read
        else:
            raise Exception(f"Invalid length type ID: {length_type_id}")

        return Result(version_total, string_reader.count + subpacket_bits_read)


with open("input.txt") as file:
    (packet,) = file.read().splitlines()

# convert hex to binary string without losing leading zeros
packet = f"{int('1' + packet, 16):b}"[1:]

result = decode(iter(packet))

print(result.version)
