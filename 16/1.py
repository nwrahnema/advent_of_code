from itertools import islice
from typing import Iterator


class StringReader:
    def __init__(self, string_iter: Iterator[str]):
        self.string_iter = string_iter
        self.count = 0

    def take(self, n: int) -> str:
        self.count += n
        return "".join(islice(self.string_iter, n))


def decode(packet: Iterator[str]) -> tuple[int, int]:
    string_reader = StringReader(packet)

    version = int(string_reader.take(3), 2)
    type_id = string_reader.take(3)
    if type_id == "100":
        literal_value = ""

        is_last = False
        while not is_last:
            is_last = string_reader.take(1) == "0"
            literal_value += string_reader.take(4)

        return version, string_reader.count
    else:
        length_type_id = string_reader.take(1)
        subpacket_bits_read = 0

        def read_subpacket():
            nonlocal version, subpacket_bits_read

            subpacket_version, bits_read = decode(packet)
            version += subpacket_version
            subpacket_bits_read += bits_read

        if length_type_id == "0":
            length = int(string_reader.take(15), 2)

            while subpacket_bits_read < length:
                read_subpacket()

            return version, string_reader.count + subpacket_bits_read
        elif length_type_id == "1":
            num_subpackets = int(string_reader.take(11), 2)

            for _ in range(num_subpackets):
                read_subpacket()

            return version, string_reader.count + subpacket_bits_read


with open("input.txt") as file:
    (packet,) = file.read().splitlines()

# convert hex to binary string without losing leading zeros
packet = f"{int('1' + packet, 16):b}"[1:]

version, _ = decode(iter(packet))

print(version)
