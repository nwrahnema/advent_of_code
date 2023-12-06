from dataclasses import dataclass
from itertools import chain
from typing import Iterator, Union

PIXEL_MAP = {".": "0", "#": "1"}


@dataclass
class PixelRow:
    pixels: str

    def __len__(self) -> int:
        return len(self.pixels)

    def __iter__(self) -> Iterator[str]:
        return self.pixels.__iter__()

    def __getitem__(self, key: Union[int, slice]) -> str:
        if isinstance(key, slice):
            return "".join(
                self.__getitem__(i)
                for i in range(
                    key.start or 0, key.stop or len(self.pixels), key.step or 1
                )
            )
        elif isinstance(key, int):
            if 0 <= key < len(self.pixels):
                return self.pixels[key]
            return " "
        raise TypeError("Invalid argument type", key)

    def __str__(self) -> str:
        return self.pixels


@dataclass
class Image:
    rows: list[PixelRow]

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self) -> Iterator[PixelRow]:
        return self.rows.__iter__()

    def __getitem__(
        self, key: Union[int, slice]
    ) -> Union[PixelRow, Iterator[PixelRow]]:
        if isinstance(key, slice):
            return (
                self.__getitem__(i)
                for i in range(
                    key.start or 0, key.stop or len(self.rows), key.step or 1
                )
            )
        elif isinstance(key, int):
            if 0 <= key < len(self.rows):
                return self.rows[key]
            return PixelRow("")
        raise TypeError("Invalid argument type", key)

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.rows)


def enhance_image(image: Image, enhance_key: str, void: str) -> Image:
    rows: list[list[str]] = []
    for i in range(-1, len(image) + 1):
        row: list[str] = []
        for j in range(-1, len(image[0]) + 1):
            key = list(
                chain.from_iterable(image[k][j - 1 : j + 2] for k in (i - 1, i, i + 1))
            )
            key = int("".join(PIXEL_MAP.get(char, PIXEL_MAP[void]) for char in key), 2)
            pixel = enhance_key[key]
            row.append(pixel)
        rows.append(row)
    return Image([PixelRow("".join(row)) for row in rows])


def main() -> None:
    with open("input.txt") as file:
        enhance_key, image = file.read().split("\n\n")
        image = Image([PixelRow(pixels) for pixels in image.split("\n")])

    void = "."
    for _ in range(50):
        image = enhance_image(image, enhance_key, void)
        void = enhance_key[0] if void == "." else enhance_key[511]
    print(sum(pixel == "#" for row in image for pixel in row))


if __name__ == "__main__":
    main()
