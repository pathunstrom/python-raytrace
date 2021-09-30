from __future__ import annotations

from .tuples import Color


class Canvas:

    def __init__(self, width: int, height: int):
        self.pixels: list[Color] = [Color(0, 0, 0) for _ in range(width * height)]
        self.width: int = width
        self.height: int = height

    def __iter__(self):
        yield from self.pixels

    def __getitem__(self, item: tuple[int, int]) -> Color:
        return self.pixels[self._coordinate_to_index(*item)]

    def __setitem__(self, key: tuple[int, int], value: Color):
        self.pixels[self._coordinate_to_index(*key)] = value

    def _coordinate_to_index(self, x, y):
        return x + (y * self.width)
