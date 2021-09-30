from __future__ import annotations

from pathlib import Path
from typing import Union

from .tuples import Color


class Canvas:

    def __init__(self, width: int, height: int, default: Color = Color(0, 0, 0)):
        self.pixels: list[Color] = [default for _ in range(width * height)]
        self.width: int = width
        self.height: int = height

    def __iter__(self):
        yield from self.pixels

    def __getitem__(self, item: tuple[int, int]) -> Color:
        return self.pixels[self._coordinate_to_index(*item)]

    def __setitem__(self, key: tuple[int, int], value: Color):
        self.pixels[self._coordinate_to_index(*key)] = value

    def save(self, file_path: Union[Path, str]):
        with open(file_path, "w") as ppm:
            lines = ["P3\n", f"{self.width} {self.height}\n", "255\n"]
            for offset in range(0, ((self.height - 1) * self.width) + 1, self.width):
                line_pixels = []
                line_pixels_total_characters = 0
                for pixel in self.pixels[offset:offset + self.width]:
                    for element in pixel:
                        element = min(max(round(element * 255), 0), 255)
                        element_string = str(element)
                        element_length = len(element_string)
                        if line_pixels_total_characters + element_length + len(line_pixels) > 70:
                            line = " ".join(line_pixels)
                            line += "\n"
                            lines.append(line)
                            line_pixels = []
                            line_pixels_total_characters = 0
                        line_pixels.append(element_string)
                        line_pixels_total_characters += element_length
                line = " ".join(line_pixels)
                line += "\n"
                lines.append(line)
            ppm.writelines(lines)

    def _coordinate_to_index(self, x, y):
        return x + (y * self.width)
